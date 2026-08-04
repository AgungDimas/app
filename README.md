# 🤖 AI-Driven Tech Assessment Portal

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

A lightweight, high-performance web application designed to simulate automated technical interviews. Built as a Research & Development (R&D) Proof of Concept, this app evaluates technical answers using a rule-based AI scoring engine and provides real-time, dynamic feedback to candidates.

## ✨ Key Features

- **🪄 Single Page Application (SPA) Experience:** Seamless transitions between Welcome, Assessment, and Result screens without page reloads using Vanilla JS.
- **🧠 Automated Rule-Based Evaluation:** Backend engine that analyzes text input to detect keywords and context.
- **⚡ Low-Latency API:** Built with Flask for lightning-fast request handling and JSON responses.
- **🎨 Modern UI/UX:** Clean, responsive, and intuitive interface designed with raw CSS (No heavy UI frameworks required).
- **📊 Dynamic Scoring System:** Automatically calculates scores (0-100) and assigns candidate statuses (Excellent, Average, Below Standard).

## 🛠️ Tech Stack

- **Backend:** Python, Flask (RESTful API)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Architecture:** Decoupled Logic (UI rendered via template string, Data processed via JSON API).

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites
Make sure you have Python installed on your system.
```bash
python --version
```

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-tech-assessment.git
   cd ai-tech-assessment
   ```

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install flask
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the Web App:**
   Open your browser and navigate to: `http://127.0.0.1:5000`

## 📡 API Reference

This application uses a RESTful approach. You can bypass the UI and hit the API directly using Postman or cURL.

**Endpoint:** `POST /api/submit_test`

**Request Payload Example:**
```json
{
  "nama_kandidat": "BungDimas",
  "jawaban1": "Application Programming Interface",
  "jawaban2": "Python and Node",
  "jawaban3": "git push",
  "jawaban4": "SELECT",
  "jawaban5": "Python"
}
```

**Response Example:**
```json
{
  "kandidat": "BungDimas",
  "skor_akhir": 100,
  "status": "🌟 Lulus (Excellent)",
  "evaluasi_detail": [
    {
      "komentar": "Tepat sekali! Itu kepanjangan dari API.",
      "poin": 20
    }
  ]
}
```

## 👨‍💻 Author

**BungDimas**  
*R&D Intern | Full-Stack Enthusiast*  
Feel free to reach out or connect with me if you have any questions or feedback regarding this project!
