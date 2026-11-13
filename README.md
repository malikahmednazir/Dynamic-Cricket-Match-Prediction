# Dynamic Cricket Outcome Prediction

This project implements a reproducible ball-by-ball second-innings classifier inspired by Goel et al. (2021), DOI: 10.3233/JSA-200510.

## Files expected
Put these ZIP files in the same folder as `cricket_prediction.py`:
- `archive (1).zip` — must contain `match_info_data.csv` and `match_data.csv` (IPL)
- `archive.zip` — must contain `matches.csv` and `ball_by_ball_data.csv` (IPL + PSL)

## Install and run (Windows PowerShell)
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python cricket_prediction.py
```

Only run PSL:
```powershell
python cricket_prediction.py --skip-ipl
```

Only run IPL:
```powershell
python cricket_prediction.py --skip-psl
```

PSL default test is the latest season present in the archive. Override it:
```powershell
python cricket_prediction.py --skip-ipl --psl-test-season 2025
```

## Outputs
Created under `outputs/`:
- `ball_level_features.csv`
- `model_metrics.csv`
- per-model confusion matrix PNGs
- `metrics_comparison.png`
- `roc_curves.png`

## Research integrity notes
The paper says 90 macro-generated attributes were reduced to 30 using wrapper feature selection, but the pasted article does not disclose the full Excel macro logic or an exact column-by-column list of the selected 30 fields. This implementation creates transparent cumulative batter/bowler and live-chase features from the available delivery data, then selects up to 30 features using mutual information on training data only. It is therefore a methodology-faithful approximation, not a bit-for-bit replication of the authors' unpublished feature-engineering workbook.

The IPL archive available here has a different number of matches/ball rows than the paper's stated 692 train matches, 59 test matches, 79,129 train rows and 6,960 test rows. The script reports actual counts rather than altering data to force a match.

The two "NEW" models are ExtraTrees and HistGradientBoosting, chosen to avoid extra third-party packages. The paper baselines are SVC and Random Forest.
