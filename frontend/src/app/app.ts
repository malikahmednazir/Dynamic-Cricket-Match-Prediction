import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
 selector: 'app-root',
 standalone: true,
 imports: [CommonModule, FormsModule],
 template: `
 <header>
   <a class="logo" href="#home">🏏 CricketAI</a>
   <nav>
     <a href="#home">Home</a>
     <a href="#about">About</a>
     <a href="#dataset">Dataset</a>
     <a href="#models">Models</a>
     <a href="#prediction">Prediction</a>
     <a href="#results">Results</a>
   </nav>
 </header>

 <section id="home" class="hero">
   <div>
     <span class="tag">ARTIFICIAL INTELLIGENCE • CRICKET ANALYTICS</span>
     <h1>Dynamic Cricket<br><span>Match Prediction</span></h1>
     <p>Machine learning powered cricket analytics and match prediction platform.</p>
     <a class="btn" href="#prediction">Predict Match →</a>
   </div>
   <div class="ball">🏏</div>
 </section>

 <section id="about" class="section">
   <span class="tag">INTRODUCTION</span>
   <h2>About Our Project</h2>
   <p class="description">
     A cricket analytics project using machine learning techniques
     to study match performance and predict cricket outcomes.
   </p>
   <div class="grid">
     <article class="card"><h3>📊 Data Analysis</h3><p>Analyze cricket statistics and match information.</p></article>
     <article class="card"><h3>🤖 Machine Learning</h3><p>Explore trained predictive models and their performance.</p></article>
     <article class="card"><h3>⚡ Dynamic Prediction</h3><p>Interactive match input and prediction interface.</p></article>
   </div>
 </section>

 <section id="dataset" class="section alternate">
   <span class="tag">DATA MANAGEMENT</span>
   <h2>Dataset & Features</h2>
   <p class="description">
     Cricket data is used for training, evaluation and predictive analysis.
     Dataset statistics will be displayed when the original dataset is connected.
   </p>
   <div class="grid">
     <article class="card"><h3>Match Data</h3><p>Teams and match information.</p></article>
     <article class="card"><h3>Performance</h3><p>Runs, wickets and overs.</p></article>
     <article class="card"><h3>Feature Engineering</h3><p>Preparing data for model input.</p></article>
   </div>
 </section>

 <section id="models" class="section">
   <span class="tag">MACHINE LEARNING</span>
   <h2>Implemented Model Architecture</h2>
   <p class="description">
     The project model list is presented below. Actual trained model files
     and evaluation results must be connected to verify live execution.
   </p>
   <div class="grid">
     <article class="card model"><span>01</span><h3>Support Vector Classifier</h3><p>SVC machine learning approach.</p></article>
     <article class="card model"><span>02</span><h3>Random Forest</h3><p>Tree-based ensemble learning.</p></article>
     <article class="card model"><span>03</span><h3>CatBoost</h3><p>Gradient boosting framework.</p></article>
     <article class="card model"><span>04</span><h3>LightGBM</h3><p>Efficient gradient boosting.</p></article>
   </div>
 </section>

 <section id="prediction" class="section alternate">
   <span class="tag">INTERACTIVE PREDICTION</span>
   <h2>Cricket Match Prediction</h2>
   <p class="description">Enter the five match parameters below.</p>

   <div class="formbox">
     <label>1. Batting Team</label>
     <input [(ngModel)]="batting" placeholder="Enter batting team">

     <label>2. Bowling Team</label>
     <input [(ngModel)]="bowling" placeholder="Enter bowling team">

     <label>3. Current Score (Runs)</label>
     <input type="number" [(ngModel)]="score" min="0" placeholder="e.g. 125">

     <label>4. Overs Completed</label>
     <input type="number" [(ngModel)]="overs" min="0" max="20" step="0.1" placeholder="e.g. 15">

     <label>5. Wickets Lost</label>
     <input type="number" [(ngModel)]="wickets" min="0" max="10" placeholder="e.g. 4">

     <button class="btn full" (click)="submitPrediction()">Submit Prediction</button>

     <div class="notice" *ngIf="message">
       {{message}}
     </div>
   </div>
 </section>

 <section id="results" class="section">
   <span class="tag">MATCH ANALYTICS</span>
   <h2>Prediction Results</h2>
   <div class="resultbox">
     <h3>Prediction Dashboard</h3>
     <p>Actual model output, accuracy and evaluation metrics will appear here after connecting the trained models.</p>
     <p><strong>Model status:</strong> Awaiting trained model integration.</p>
   </div>
 </section>

 <section id="contact" class="section alternate">
   <span class="tag">PROJECT INFORMATION</span>
   <h2>Explore Our Project</h2>
   <p class="description">Dynamic Cricket Match Prediction</p>
   <a class="btn" href="https://github.com/malikahmednazir/Dynamic-Cricket-Match-Prediction" target="_blank">View GitHub Repository</a>
 </section>

 <footer>
   <h3>🏏 CricketAI</h3>
   Dynamic Cricket Match Prediction | 2026
 </footer>
 `,
 styles: [`
 *{box-sizing:border-box;scroll-behavior:smooth}
 :host{display:block;background:#08131f;color:#f3f7fa;font-family:Arial,sans-serif}
 header{position:sticky;top:0;z-index:20;background:#102333;padding:20px 6%;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}
 .logo{font-size:24px;font-weight:bold;color:#44e0a1;text-decoration:none}
 nav{display:flex;gap:19px;flex-wrap:wrap}
 nav a{color:#e6edf3;text-decoration:none;font-size:14px}
 nav a:hover{color:#44e0a1}
 .hero{min-height:530px;padding:100px 9%;display:flex;align-items:center;justify-content:space-between;gap:25px;background:linear-gradient(120deg,#123b39,#08131f)}
 .hero h1{font-size:clamp(38px,6vw,68px);line-height:1.1}
 .hero h1 span{color:#44e0a1}
 .hero p,.description{color:#b0c0cc;line-height:1.8;max-width:750px}
 .ball{font-size:130px}
 .tag{color:#44e0a1;font-size:12px;font-weight:bold;letter-spacing:2px}
 .btn{display:inline-block;background:#44e0a1;color:#08131f;padding:15px 25px;border:0;border-radius:7px;text-decoration:none;font-weight:bold;cursor:pointer;margin-top:18px}
 .section{padding:85px 9%}
 .section h2{font-size:36px;margin:15px 0}
 .alternate{background:#102333}
 .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px;margin-top:35px}
 .card{padding:28px;background:#142b3d;border:1px solid #2c4657;border-radius:12px}
 .card h3{color:#44e0a1}
 .card p{color:#b1c1ce;line-height:1.7}
 .model span{color:#44e0a1;font-size:26px;font-weight:bold}
 .formbox,.resultbox{max-width:650px;background:#142b3d;border:1px solid #304a5b;padding:30px;border-radius:12px;margin-top:30px}
 .formbox label{display:block;margin:18px 0 8px}
 .formbox input{width:100%;padding:14px;background:#08131f;color:white;border:1px solid #365467;border-radius:6px;font-size:15px}
 .full{width:100%;margin-top:25px}
 .notice{margin-top:20px;padding:15px;background:#263e43;border-radius:7px;line-height:1.6}
 .resultbox p{color:#b1c1ce;line-height:1.7}
 footer{text-align:center;padding:35px;background:#06101a;color:#9eb0bf}
 @media(max-width:650px){header{justify-content:center}nav{justify-content:center;gap:12px}.hero{padding:70px 7%}.ball{display:none}.section{padding:65px 7%}}
 `]
})
export class App {
 batting = '';
 bowling = '';
 score: number | null = null;
 overs: number | null = null;
 wickets: number | null = null;
 message = '';

 submitPrediction() {
   if (!this.batting.trim() || !this.bowling.trim()) {
     this.message = 'Please enter both team names.';
     return;
   }
   if (this.score === null || this.overs === null || this.wickets === null ||
       !Number.isFinite(this.score) || !Number.isFinite(this.overs) ||
       !Number.isInteger(this.wickets) || this.score < 0 ||
       this.overs < 0 || this.overs > 20 ||
       this.wickets < 0 || this.wickets > 10) {
     this.message = 'Please enter valid values for all five parameters.';
     return;
   }
   this.message = 'Your five parameters have been captured. Connect the original trained Python model API to generate a real prediction. GitHub Pages cannot execute Python models.';
 }
}
