#!/usr/bin/env python
"""
Dynamic cricket match outcome prediction
Implements a ball-by-ball second-innings pipeline inspired by:
Goel et al. (2021), Journal of Sports Analytics 7(3), 185-196.
DOI: 10.3233/JSA-200510

Supported input archives:
  archive (1).zip: match_info_data.csv + match_data.csv (IPL)
  archive.zip: matches.csv + ball_by_ball_data.csv (IPL + PSL)

Important:
The paper's Excel macros and exact selected 30-column feature list are not
fully specified in the pasted article text. This is a transparent,
reproducible approximation of the described player/innings features, not a
claim of bit-for-bit reproduction of the authors' private feature pipeline.
"""
from __future__ import annotations
import argparse, zipfile, warnings
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, HistGradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix, ConfusionMatrixDisplay,
                             classification_report, roc_curve)
from sklearn.model_selection import TimeSeriesSplit, cross_val_score

warnings.filterwarnings("ignore")
RANDOM_STATE = 42

def read_csv_from_zip(zip_path: Path, member: str) -> pd.DataFrame:
    with zipfile.ZipFile(zip_path) as z:
        candidates = [n for n in z.namelist() if Path(n).name.lower() == member.lower()]
        if not candidates:
            raise FileNotFoundError(f"{member} not found inside {zip_path}")
        with z.open(candidates[0]) as f:
            return pd.read_csv(f, low_memory=False)

def load_ipl_archive1(path: Path):
    matches = read_csv_from_zip(path, "match_info_data.csv")
    balls = read_csv_from_zip(path, "match_data.csv")
    matches = matches.rename(columns={"id":"match_id", "winner":"winner"})
    balls = balls.rename(columns={"runs_off_bat":"runs_off_bat"})
    return matches, balls, "ipl"

def load_cricsheet_archive(path: Path, league: str):
    matches = read_csv_from_zip(path, "matches.csv")
    balls = read_csv_from_zip(path, "ball_by_ball_data.csv")
    matches = matches[matches["collection"].astype(str).str.lower().eq(league)].copy()
    balls = balls[balls["match_id"].isin(matches["match_id"])].copy()
    matches = matches.rename(columns={"team_1":"team1", "team_2":"team2"})
    return matches, balls, league

def normalize_season(x):
    s = str(x).strip()
    try:
        # preserve IPL's 2007/08 as the start year 2008 for split purposes
        if "/" in s:
            a, b = s.split("/")[:2]
            # IPL/PSL season labels such as 2007/08 are mapped to ending year 2008.
            return (2000 + int(b)) if len(b) == 2 else int(b)
        return int(float(s))
    except Exception:
        return pd.to_datetime(s, errors="coerce").year

def get_match_winner_map(matches):
    m = matches.copy()
    if "match_id" not in m:
        raise ValueError("Matches file must contain match_id")
    if "winner" not in m:
        raise ValueError("Matches file must contain winner")
    return dict(zip(m.match_id, m.winner))

def build_ball_level_dataset(matches: pd.DataFrame, balls: pd.DataFrame, league: str):
    """Build one row after every second-innings delivery."""
    required = {"match_id", "innings", "batting_team", "bowling_team",
                "striker", "bowler", "runs_off_bat", "extras"}
    missing = required - set(balls.columns)
    if missing:
        raise ValueError(f"Ball file missing required columns: {sorted(missing)}")

    b = balls.copy()
    b["innings"] = pd.to_numeric(b["innings"], errors="coerce")
    b = b[b.innings.isin([1, 2])].copy()
    b["runs_off_bat"] = pd.to_numeric(b["runs_off_bat"], errors="coerce").fillna(0)
    b["extras"] = pd.to_numeric(b["extras"], errors="coerce").fillna(0)
    b["total_runs"] = b["runs_off_bat"] + b["extras"]
    if "wicket" in b:
        b["is_wicket"] = pd.to_numeric(b["wicket"], errors="coerce").fillna(0).astype(int)
    else:
        b["is_wicket"] = b.get("player_dismissed", pd.Series(index=b.index)).notna().astype(int)
    if "delivery_number" in b:
        b = b.sort_values(["match_id", "innings", "delivery_number"])
    elif "ball" in b:
        b["_ball_sort"] = pd.to_numeric(b["ball"], errors="coerce")
        b = b.sort_values(["match_id", "innings", "_ball_sort"])
    else:
        b = b.sort_values(["match_id", "innings"])

    # season is sourced from match data; fallback to start_date.
    season_map = {}
    if "season" in matches:
        season_map = dict(zip(matches.match_id, matches.season))
    winner_map = get_match_winner_map(matches)

    rows = []
    for mid, game in b.groupby("match_id", sort=False):
        first = game[game.innings == 1]
        second = game[game.innings == 2]
        if first.empty or second.empty:
            continue
        batting_team = str(second.iloc[0]["batting_team"])
        winner = winner_map.get(mid)
        if pd.isna(winner) or winner is None or str(winner).strip() == "":
            continue
        # Exclude ties/no-results and matches where winner is not one of the innings teams.
        if str(winner) not in set(game["batting_team"].astype(str).unique()):
            continue
        # DLS-affected games are excluded because target revisions are not fully
        # represented consistently in both source schemas.
        match_row = matches[matches.match_id == mid]
        if not match_row.empty:
            mr = match_row.iloc[0]
            dl = mr.get("dl_applied", 0)
            method = str(mr.get("result_method", "")).lower()
            if str(dl).lower() in ("1", "true", "yes") or method in ("d/l", "dl", "duckworth-lewis"):
                continue
        target = int(first["total_runs"].sum()) + 1
        season_raw = season_map.get(mid, second.iloc[0].get("season", np.nan))
        season = normalize_season(season_raw)
        # Stable player slots: order of first appearance in the chase.
        batter_slots = {}
        bowler_slots = {}
        batter_runs = {}
        bowler_runs = {}
        score = wickets = legal_balls = 0
        for _, d in second.iterrows():
            striker = str(d["striker"])
            bowler = str(d["bowler"])
            if striker not in batter_slots and len(batter_slots) < 11:
                batter_slots[striker] = len(batter_slots) + 1
            if bowler not in bowler_slots and len(bowler_slots) < 10:
                bowler_slots[bowler] = len(bowler_slots) + 1
            batter_runs[striker] = batter_runs.get(striker, 0) + float(d["runs_off_bat"])
            bowler_runs[bowler] = bowler_runs.get(bowler, 0) + float(d["total_runs"])
            score += int(d["total_runs"])
            wickets += int(d["is_wicket"])
            # Wide deliveries do not count as legal balls; no-ball normally does not either.
            is_legal = True
            if "is_legal_delivery" in second.columns:
                is_legal = bool(d.get("is_legal_delivery", True))
            elif "wides" in second.columns or "noballs" in second.columns:
                is_legal = not (float(d.get("wides", 0) or 0) > 0 or float(d.get("noballs", 0) or 0) > 0)
            if is_legal:
                legal_balls += 1
            over_no = min(20, legal_balls // 6)
            balls_left = max(0, 120 - legal_balls)
            row = {
                "match_id": mid, "season": season, "over": over_no,
                "ball_in_innings": legal_balls, "balls_left": balls_left,
                "wickets_left": max(0, 10 - wickets), "present_score": score,
                "target": target, "runs_needed": max(0, target - score),
                "run_rate": score / max(legal_balls / 6, 1/6),
                "required_run_rate": max(0, target-score) / max(balls_left/6, 1/6),
                "this_ball_batter_runs": float(d["runs_off_bat"]),
                "this_ball_extras": float(d["extras"]),
                "total_runs_this_ball": float(d["total_runs"]),
                "wickets_this_ball": int(d["is_wicket"]),
                "batting_team": batting_team,
                "won": int(str(winner) == batting_team)
            }
            for name, slot in batter_slots.items():
                row[f"Bman{slot}_runs"] = batter_runs.get(name, 0)
            for name, slot in bowler_slots.items():
                row[f"Bowl{slot}_runs"] = bowler_runs.get(name, 0)
            rows.append(row)
            # Stop at first completed chase to avoid adding post-result deliveries.
            if score >= target or wickets >= 10 or legal_balls >= 120:
                break

    data = pd.DataFrame(rows)
    if data.empty:
        raise ValueError("No usable second-innings rows found. Check league name and input files.")
    # Keep only rows for matches with a decisive result; remove raw identifiers from predictors.
    data = data.sort_values(["season", "match_id", "ball_in_innings"]).reset_index(drop=True)
    return data

def make_models():
    return {
        "SVC": SVC(C=1.0, kernel="rbf", probability=True, class_weight="balanced",
                   random_state=RANDOM_STATE),
        "RandomForest": RandomForestClassifier(n_estimators=350, min_samples_leaf=2,
                    max_features="sqrt", class_weight="balanced_subsample",
                    n_jobs=-1, random_state=RANDOM_STATE),
        "ExtraTrees_NEW": ExtraTreesClassifier(n_estimators=350, min_samples_leaf=2,
                    max_features="sqrt", class_weight="balanced", n_jobs=-1,
                    random_state=RANDOM_STATE),
        "HistGradientBoosting_NEW": HistGradientBoostingClassifier(max_iter=220,
                    learning_rate=0.06, max_leaf_nodes=15, l2_regularization=1.0,
                    random_state=RANDOM_STATE)
    }

def evaluate_one(name, model, X_train, y_train, X_test, y_test, outdir):
    numeric = list(X_train.columns)
    prep = Pipeline([("imputer", SimpleImputer(strategy="median")),
                     ("scale", StandardScaler())])
    pipe = Pipeline([("prep", prep),
                     ("select", SelectKBest(score_func=mutual_info_classif,
                                             k=min(30, len(numeric)))),
                     ("model", model)])
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    if hasattr(pipe, "predict_proba"):
        prob = pipe.predict_proba(X_test)[:, 1]
    elif hasattr(pipe, "decision_function"):
        raw = pipe.decision_function(X_test)
        prob = (raw - raw.min()) / (raw.max() - raw.min() + 1e-9)
    else:
        prob = pred.astype(float)
    metrics = {
        "Model": name,
        "Accuracy": accuracy_score(y_test, pred),
        "Precision": precision_score(y_test, pred, zero_division=0),
        "Recall": recall_score(y_test, pred, zero_division=0),
        "F1": f1_score(y_test, pred, zero_division=0),
        "ROC_AUC": roc_auc_score(y_test, prob) if len(np.unique(y_test)) == 2 else np.nan
    }
    cm = confusion_matrix(y_test, pred, labels=[0,1])
    fig, ax = plt.subplots(figsize=(5,4))
    ConfusionMatrixDisplay(cm, display_labels=["Lose", "Win"]).plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(f"{name} - Confusion Matrix")
    fig.tight_layout(); fig.savefig(outdir / f"{name}_confusion_matrix.png", dpi=160); plt.close(fig)
    fpr, tpr, _ = roc_curve(y_test, prob)
    return metrics, (fpr, tpr), pipe

def run_experiment(matches, balls, league, train_end=None, test_season=None):
    outdir = Path("outputs") / league.upper()
    outdir.mkdir(parents=True, exist_ok=True)
    data = build_ball_level_dataset(matches, balls, league)
    data.to_csv(outdir / "ball_level_features.csv", index=False)

    # IPL paper split: seasons 2008-2018 train, 2019 test.
    if league.lower() == "ipl":
        train_end = 2018 if train_end is None else train_end
        test_season = 2019 if test_season is None else test_season
        train = data[data.season <= train_end].copy()
        test = data[data.season == test_season].copy()
    else:
        # PSL: chronological holdout by latest available season.
        latest = int(data.season.max()) if test_season is None else int(test_season)
        test_season = latest
        train = data[data.season < latest].copy()
        test = data[data.season == latest].copy()
    if train.empty or test.empty:
        raise ValueError(f"Empty split: train rows={len(train)}, test rows={len(test)}. "
                         f"Available seasons: {sorted(data.season.dropna().unique())}")

    # Remove identifiers/team labels to avoid memorizing match/team identity.
    drop_cols = {"won", "match_id", "season", "batting_team"}
    feature_cols = [c for c in data.columns if c not in drop_cols and
                    pd.api.types.is_numeric_dtype(data[c])]
    X_train, y_train = train[feature_cols], train["won"].astype(int)
    X_test, y_test = test[feature_cols], test["won"].astype(int)
    if y_train.nunique() < 2 or y_test.nunique() < 2:
        raise ValueError("Both classes (win and lose) must exist in train and test split.")

    print(f"\n{league.upper()} | train seasons <= {train_end if league=='ipl' else '< '+str(test_season)}"
          f" | test season = {test_season}")
    print(f"Rows: train={len(train):,}, test={len(test):,}; features={len(feature_cols)}")
    print(f"Unique matches: train={train.match_id.nunique()}, test={test.match_id.nunique()}")

    # TimeSeriesSplit CV on training data only, in chronological row order.
    # CV score is reported as a diagnostic; final test is the untouched season.
    cv_model = RandomForestClassifier(n_estimators=160, min_samples_leaf=2,
                    class_weight="balanced_subsample", n_jobs=-1, random_state=RANDOM_STATE)
    cv_pipe = Pipeline([("imputer", SimpleImputer(strategy="median")),
                        ("select", SelectKBest(mutual_info_classif, k=min(30,len(feature_cols)))),
                        ("model", cv_model)])
    n_splits = min(5, max(2, train.match_id.nunique() // 10))
    try:
        cv = TimeSeriesSplit(n_splits=n_splits)
        cv_scores = cross_val_score(cv_pipe, X_train, y_train, cv=cv, scoring="accuracy", n_jobs=1)
        print(f"TimeSeriesSplit CV accuracy: {cv_scores.mean():.4f} +/- {cv_scores.std():.4f}")
    except Exception as e:
        print("CV skipped:", e)

    results, roc_data = [], {}
    for name, model in make_models().items():
        print("Training", name)
        met, roc_pair, fitted = evaluate_one(name, model, X_train, y_train, X_test, y_test, outdir)
        results.append(met); roc_data[name] = roc_pair

    res = pd.DataFrame(results).sort_values("Accuracy", ascending=False)
    res.to_csv(outdir / "model_metrics.csv", index=False)
    print("\nTEST RESULTS")
    print(res.to_string(index=False, float_format=lambda x: f"{x:.4f}"))

    # Metric comparison chart
    metric_cols = ["Accuracy", "Precision", "Recall", "F1", "ROC_AUC"]
    ax = res.set_index("Model")[metric_cols].plot(kind="bar", figsize=(12,6), ylim=(0,1))
    ax.set_title(f"{league.upper()} model comparison")
    ax.set_ylabel("Score"); ax.set_xlabel("")
    plt.xticks(rotation=20, ha="right"); plt.tight_layout()
    plt.savefig(outdir / "metrics_comparison.png", dpi=170); plt.close()

    # ROC curves
    fig, ax = plt.subplots(figsize=(7,6))
    for name, (fpr, tpr) in roc_data.items():
        auc = res.loc[res.Model == name, "ROC_AUC"].iloc[0]
        ax.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")
    ax.plot([0,1],[0,1],"k--",linewidth=1)
    ax.set(xlabel="False Positive Rate", ylabel="True Positive Rate",
           title=f"{league.upper()} ROC curves", xlim=(0,1), ylim=(0,1))
    ax.legend(); plt.tight_layout()
    plt.savefig(outdir / "roc_curves.png", dpi=170); plt.close()
    print(f"\nSaved outputs to: {outdir.resolve()}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ipl-zip", default="archive (1).zip",
                    help="IPL zip with match_info_data.csv and match_data.csv")
    ap.add_argument("--combined-zip", default="archive.zip",
                    help="Cricsheet zip with matches.csv and ball_by_ball_data.csv")
    ap.add_argument("--skip-ipl", action="store_true")
    ap.add_argument("--skip-psl", action="store_true")
    ap.add_argument("--psl-test-season", type=int, default=None)
    args = ap.parse_args()

    if not args.skip_ipl:
        p = Path(args.ipl_zip)
        if p.exists():
            m, b, league = load_ipl_archive1(p)
            run_experiment(m, b, league)
        else:
            print(f"IPL archive not found: {p}; skipping IPL.")
    if not args.skip_psl:
        p = Path(args.combined_zip)
        if p.exists():
            m, b, league = load_cricsheet_archive(p, "psl")
            run_experiment(m, b, league, test_season=args.psl_test_season)
        else:
            print(f"Combined archive not found: {p}; skipping PSL.")

if __name__ == "__main__":
    main()
