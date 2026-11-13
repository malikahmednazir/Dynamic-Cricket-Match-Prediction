import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <nav class="navbar">
      <a class="brand" href="#home">🏏 CricketAI</a>
      <div class="navlinks">
        <a href="#home">Home</a>
        <a href="#about">About</a>
        <a href="#dataset">Dataset</a>
        <a href="#models">Models</a>
        <a href="#prediction">Prediction</a>
        <a href="#contact">Contact</a>
      </div>
    </nav>

    <section id="home" class="hero">
      <div class="hero-content">
        <span class="tag">MACHINE LEARNING PROJECT</span>
        <h1>Dynamic Cricket<br><span>Match Prediction</span></h1>
        <p>Explore cricket analytics and machine learning powered match prediction.</p>
        <a class="primary-btn" href="#prediction">Try Prediction →</a>
      </div>
      <div class="hero-icon">🏏</div>
    </section>

    <section id="about" class="section">
      <span class="tag">INTRODUCTION</span>
      <h2>About The Project</h2>
      <p class="description">
        Dynamic Cricket Match Prediction is a machine learning project
        designed to analyze cricket match information and support
        data-driven predictions.
      </p>
      <div class="cards">
        <article class="card">
          <div class="card-icon">📊</div>
          <h3>Data Analysis</h3>
          <p>Explore match statistics, teams and cricket data.</p>
        </article>
        <article class="card">
          <div class="card-icon">🤖</div>
          <h3>Machine Learning</h3>
          <p>Build predictive systems using trained machine learning models.</p>
        </article>
        <article class="card">
          <div class="card-icon">⚡</div>
          <h3>Dynamic Prediction</h3>
          <p>Submit match information through an interactive interface.</p>
        </article>
      </div>
    </section>

    <section id="dataset" class="section dark-section">
      <span class="tag">DATA</span>
      <h2>Dataset Overview</h2>
      <p class="description">
        The project dataset is used for cricket data analysis and
        machine learning experiments.
      </p>
      <div class="cards">
        <article class="card">
          <h3>Match Information</h3>
          <p>Team names, match details and other available match attributes.</p>
        </article>
        <article class="card">
          <h3>Performance Data</h3>
          <p>Cricket performance information used by the project.</p>
        </article>
        <article class="card">
          <h3>Data Processing</h3>
          <p>Prepare and transform data for machine learning.</p>
        </article>
      </div>
      <p class="note">Actual dataset statistics will be displayed after the dataset is connected.</p>
    </section>

    <section id="models" class="section">
      <span class="tag">TECHNOLOGY</span>
      <h2>Machine Learning Models</h2>
      <p class="description">
        The backend can be connected to the trained models available in your project.
      </p>
      <div class="cards">
        <article class="card">
          <div class="card-icon">🌳</div>
          <h3>Random Forest</h3>
          <p>Ensemble learning approach for predictive analysis.</p>
        </article>
        <article class="card">
          <div class="card-icon">📈</div>
          <h3>Classification</h3>
          <p>Machine learning classification for prediction tasks.</p>
        </article>
        <article class="card">
          <div class="card-icon">🧠</div>
          <h3>Model Evaluation</h3>
          <p>Evaluate trained models using suitable performance metrics.</p>
        </article>
      </div>
      <p class="note">These are technology descriptions, not confirmation that all three models are trained.</p>
    </section>

    <section id="prediction" class="section prediction-section">
      <span class="tag">INTERACTIVE TOOL</span>
      <h2>Cricket Match Prediction</h2>
      <p class="description">Enter match details to send a prediction request to the Python backend.</p>

      <div class="prediction-box">
        <label>Team 1</label>
        <input [(ngModel)]="team1" placeholder="e.g. Pakistan">

        <label>Team 2</label>
        <input [(ngModel)]="team2" placeholder="e.g. India">

        <label>Overs completed</label>
        <input type="number" [(ngModel)]="overs" min="0" max="50">

        <label>Wickets lost</label>
        <input type="number" [(ngModel)]="wickets" min="0" max="10">

        <button class="primary-btn full" (click)="predict()" [disabled]="loading">
          {{ loading ? 'Processing...' : 'Submit Prediction' }}
        </button>

        <div class="result" *ngIf="message">
          <h3>Prediction Response</h3>
          <p>{{ message }}</p>
        </div>
      </div>
    </section>

    <section id="results" class="section">
      <span class="tag">ANALYTICS</span>
      <h2>Prediction Results</h2>
      <p class="description">
        Prediction results and evaluation metrics will appear here
        once the trained model is integrated.
      </p>
    </section>

    <section id="contact" class="section dark-section">
      <span class="tag">GET IN TOUCH</span>
      <h2>Contact</h2>
      <p class="description">
        Dynamic Cricket Match Prediction Project
      </p>
      <a class="primary-btn" href="https://github.com/malikahmednazir/Dynamic-Cricket-Match-Prediction" target="_blank">
        View GitHub Project
      </a>
    </section>

    <footer>
      © 2026 Dynamic Cricket Match Prediction | Powered by Angular and Python
    </footer>
  `,
  styles: [`
    * { box-sizing: border-box; scroll-behavior: smooth; }
    :host { display: block; background: #08131f; color: #f4f7fb; font-family: Arial, sans-serif; }
    .navbar { position: sticky; top: 0; z-index: 10; background: #101f2d; padding: 20px 6%; display: flex; justify-content: space-between; align-items: center; gap: 20px; flex-wrap: wrap; }
    .brand { font-size: 23px; font-weight: bold; color: #45e0a2; text-decoration: none; }
    .navlinks { display: flex; flex-wrap: wrap; gap: 20px; }
    .navlinks a { color: #e0e8ef; text-decoration: none; font-size: 14px; }
    .navlinks a:hover { color: #45e0a2; }
    .hero { min-height: 490px; padding: 100px 9%; display: flex; align-items: center; justify-content: space-between; background: linear-gradient(120deg,#102e35,#08131f 70%); gap: 30px; }
    .hero-content { max-width: 650px; }
    .hero h1 { font-size: clamp(38px,6vw,68px); line-height: 1.12; margin: 22px 0; }
    .hero h1 span { color: #45e0a2; }
    .hero p, .description { color: #aab9c7; line-height: 1.8; max-width: 750px; }
    .hero-icon { font-size: 120px; }
    .tag { color: #45e0a2; font-weight: bold; letter-spacing: 2px; font-size: 12px; }
    .primary-btn { display: inline-block; background: #45d99b; color: #08131f; border: 0; padding: 14px 24px; margin-top: 18px; border-radius: 7px; text-decoration: none; font-weight: bold; cursor: pointer; }
    .primary-btn:disabled { opacity: .6; cursor: wait; }
    .section { padding: 85px 9%; }
    .section h2 { font-size: 36px; margin: 16px 0; }
    .dark-section { background: #101f2d; }
    .cards { display: grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap: 20px; margin-top: 35px; }
    .card { background: #142738; border: 1px solid #294354; padding: 28px; border-radius: 12px; }
    .card h3 { color: #45e0a2; }
    .card p { color: #aab9c7; line-height: 1.7; }
    .card-icon { font-size: 34px; }
    .note { color: #9aaebe; font-size: 13px; margin-top: 22px; }
    .prediction-section { background: #0d202b; }
    .prediction-box { max-width: 600px; background: #142738; border: 1px solid #294354; padding: 30px; border-radius: 12px; margin-top: 30px; }
    .prediction-box label { display: block; margin: 17px 0 8px; color: #dce7ef; }
    .prediction-box input { width: 100%; padding: 14px; background: #08131f; border: 1px solid #355166; border-radius: 6px; color: white; }
    .full { width: 100%; }
    .result { background: #203b3d; padding: 15px; border-radius: 8px; margin-top: 20px; overflow-wrap: anywhere; }
    footer { text-align: center; padding: 25px; color: #9aabba; background: #06101a; }
    @media(max-width:650px) { .navbar { justify-content: center; } .navlinks { justify-content: center; gap: 12px; } .hero { padding: 70px 7%; } .hero-icon { display: none; } .section { padding: 65px 7%; } }
  `]
})
export class App {
  team1 = '';
  team2 = '';
  overs = 10;
  wickets = 2;
  loading = false;
  message = '';

  async predict() {
    if (!this.team1.trim() || !this.team2.trim()) {
      this.message = 'Please enter both team names.';
      return;
    }

    if (this.overs < 0 || this.overs > 50 || this.wickets < 0 || this.wickets > 10) {
      this.message = 'Please enter valid overs and wickets.';
      return;
    }

    this.loading = true;
    this.message = '';

    try {
      const response = await fetch('https://YOUR-RENDER-SERVICE.onrender.com/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          team1: this.team1,
          team2: this.team2,
          overs: this.overs,
          wickets: this.wickets
        })
      });

      const data = await response.json();
      this.message = data.message || data.error || JSON.stringify(data);
    } catch {
      this.message = 'Backend is not connected yet. Deploy the Python backend and update its URL.';
    } finally {
      this.loading = false;
    }
  }
}
