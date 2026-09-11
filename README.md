# DeCognito — Open-Source Intelligence (OSINT) Aggregation Engine

<div align="center">

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

**Modular, multi-source digital footprint reconnaissance and intelligence aggregation framework.**

</div>

---

## ⚡ Overview

**DeCognito** is an automated OSINT (Open-Source Intelligence) aggregation platform designed for cybersecurity researchers, penetration testers, and threat analysts. It unifies disparate reconnaissance channels into an asynchronous pipeline with a FastAPI service layer and an intuitive Streamlit intelligence dashboard.

### Core Capabilities:
- **Username & Digital Footprint Enumeration**: Integrates with Sherlock and social connectors to identify profile footprints across 300+ platforms.
- **Infrastructure & IP Profiling**: Shodan API connector for exposed ports, SSL certs, banner grabs, and leaked cloud services.
- **Asynchronous Task Architecture**: Background scanning powered by Celery queues to process heavy enumeration tasks without blocking API consumers.
- **Structured SQLite & JSON Persistence**: Normalized storage for target scan history, risk scoring, and audit trails.
- **Interactive UI**: Streamlit application for real-time visualization of target intelligence graphs.

---

## 🏗️ Architecture

```
                      +-------------------+
                      |   Client / CLI    |
                      +---------+---------+
                                |
                                v
                      +-------------------+
                      |  FastAPI Backend  |  (/scan, /history)
                      +---------+---------+
                                |
              +-----------------+-----------------+
              |                                   |
              v                                   v
    +-------------------+               +-------------------+
    |  Celery Workers   |               |   SQLite Storage  |
    +---------+---------+               +-------------------+
              |
      +-------+-------+
      |               |
      v               v
+------------+  +------------+
|  Sherlock  |  |   Shodan   |
| Connector  |  | Connector  |
+------------+  +------------+
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- Redis (optional, for Celery distributed worker mode)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Swayam-jhaa/DeCognito.git
cd DeCognito

# Create and activate virtual environment
python -m venv venv
# Linux/macOS:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy the template configuration and supply your API keys:
```bash
cp .env.example .env
```
Edit `.env`:
```env
SHODAN_API_KEY=your_shodan_api_key
RAPIDAPI_KEY=your_rapidapi_key
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=sqlite:///./decongito.db
```

### 4. Running the Platform
**Start the FastAPI Server**:
```bash
uvicorn app.main:app --reload --port 8000
```
Interactive Swagger documentation will be available at `http://localhost:8000/docs`.

**Start the Streamlit Intelligence Dashboard**:
```bash
streamlit run streamlit_app/app.py
```

---

## 📡 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/` | `GET` | Service health check |
| `/scan/username` | `POST` | Trigger Sherlock profile scan for target handle |
| `/scan/ip` | `POST` | Query Shodan intelligence for target IP/host |
| `/history` | `GET` | Retrieve persistent scan logs & findings |

---

## ⚖️ Legal & Ethical Disclaimer

> [!WARNING]
> **DeCognito** is developed strictly for authorized security auditing, defensive reconnaissance, educational research, and personal privacy evaluations. Scanning targets without prior mutual consent is strictly prohibited and may violate computer crime regulations. Use responsibly.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
