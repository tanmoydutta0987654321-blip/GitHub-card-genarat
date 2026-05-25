# GitHub Dev Card Generator 💳✨

A premium web application that analyzes public GitHub profiles and generates beautiful, theme-customized, glassmorphic developer profile cards. 

The application utilizes **Google ADK** (Agent Development Kit) to orchestrate a reasoning agent, **Gemini 2.5 Flash** for profile analysis, **FastMCP** (Model Context Protocol) to expose modular Python tools, **FastAPI** for the backend API, and a self-contained premium **HTML/CSS/JS frontend** served via **Nginx**.

---

## 🚀 Live Cloud Run Deployments

The project is deployed on Google Cloud Run:
*   **Frontend Web App:** [https://github-card-frontend-1085248861550.us-central1.run.app](https://github-card-frontend-1085248861550.us-central1.run.app)
*   **Backend API Service:** [https://github-card-backend-1085248861550.us-central1.run.app](https://github-card-backend-1085248861550.us-central1.run.app)

---

## 🛠️ Technology Stack

*   **Orchestration & AI:** Google Agent Development Kit (ADK), Gemini 2.5 Flash
*   **Tools Protocol:** Model Context Protocol (MCP) via `fastmcp`
*   **Backend Framework:** FastAPI, Uvicorn, Python 3.12 (packaged using `uv`)
*   **Frontend UI:** Vanilla HTML5, CSS3 Custom Properties (CSS variables), JavaScript, Google Fonts (Inter)
*   **Containerization & Server:** Docker, Docker Compose, Nginx
*   **Hosting:** Google Cloud Run, Cloud Build, Artifact Registry

---

## 📂 Project Structure

```text
github-card-generator/
├── backend/
│   ├── static/cards/      # Directory where generated cards are persisted
│   ├── .gcloudignore       # Files to ignore during Cloud Build submissions
│   ├── agent.py            # ADK Agent definition and configuration
│   ├── mcp_server.py       # FastMCP tools (scrape, analyze, render, save)
│   ├── main.py             # FastAPI Server & ADK Runner loop
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Python slim image + Astral uv build setup
├── frontend/
│   ├── index.html          # Responsive glassmorphic single-page UI
│   └── Dockerfile          # Nginx Alpine image + startup envsubst script
├── docker-compose.yml      # Multi-container local orchestration
└── .env.example            # Environment configuration template
```

---

## ⚙️ Environment Variables

Copy the `.env.example` template to configure your local or container environment variables:

| Variable | Description | Required | Default |
| :--- | :--- | :--- | :--- |
| `GEMINI_API_KEY` | Google AI Studio key for profile characterization. | Yes (in production) | *Fallback to mock analysis if unset* |
| `GITHUB_TOKEN` | GitHub Personal Access Token to increase scrape rate limits. | No | *Unauthenticated scraping* |
| `BACKEND_URL` | Endpoint of the Backend API (consumed by frontend). | Yes (on Nginx start) | `http://localhost:8080` |

---

## 💻 Local Quickstart

### Option 1: Run with Docker Compose (Recommended)

1. Clone or download the repository files.
2. Build and start the services using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Open your browser and navigate to:
   *   **Frontend UI:** [http://localhost:8080](http://localhost:8080)
   *   **Backend Docs:** [http://localhost:8080/docs](http://localhost:8080/docs) (or internal container `http://localhost:8000/docs`)

### Option 2: Run Locally (Without Docker)

#### Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create and activate a Python virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate    # macOS/Linux
   ```
3. Install dependencies using `uv` (preferred) or `pip`:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8080 --reload
   ```

#### Frontend Setup
Simply open `frontend/index.html` directly in any web browser. It will fallback automatically to communicate with `http://localhost:8080` for API requests.

---

## 🚢 Google Cloud Run Deployment

To deploy both components using the `gcloud` CLI:

### 1. Pre-requisites & Repo Setup
Ensure you are authenticated and have created a Docker repository in Artifact Registry:
```bash
# Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com artifactregistry.googleapis.com

# Create Artifact Registry Repository
gcloud artifacts repositories create github-card-repo --repository-format=docker --location=us-central1
```

### 2. Deploy Backend
Submit the build to Cloud Build and deploy to Cloud Run:
```bash
# Build
gcloud builds submit --tag us-central1-docker.pkg.dev/[PROJECT_ID]/github-card-repo/github-card-backend:latest backend

# Deploy
gcloud run deploy github-card-backend \
  --image us-central1-docker.pkg.dev/[PROJECT_ID]/github-card-repo/github-card-backend:latest \
  --platform managed --allow-unauthenticated --port 8080 --region us-central1
```
*Note: Make sure to set the `GEMINI_API_KEY` env variable in the Cloud Run console or via the `--set-env-vars` flag.*

### 3. Deploy Frontend
Submit the build and deploy to Cloud Run (Nginx listens on port 80):
```bash
# Build
gcloud builds submit --tag us-central1-docker.pkg.dev/[PROJECT_ID]/github-card-repo/github-card-frontend:latest frontend

# Deploy (injecting backend URL)
gcloud run deploy github-card-frontend \
  --image us-central1-docker.pkg.dev/[PROJECT_ID]/github-card-repo/github-card-frontend:latest \
  --platform managed --allow-unauthenticated --port 80 --region us-central1 \
  --set-env-vars BACKEND_URL=https://[YOUR-BACKEND-URL]
```
