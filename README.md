# Inkloom AI — Intelligent Brand-Governance Co-Pilot (Round 2 Build)
**Team DejaVu | Round 2 — The Build (22–25 October 2026)**

> *"Not a blocker. A collaborator."* — Inkloom AI bridges high-velocity content creation and strict enterprise brand compliance across **Tone**, **Facts**, **Visual Identity**, **Accessibility (WCAG 2.1)**, and **Legal Claims**.

## 🚀 Instant Judge Evaluation (Zero Setup Required)
1. **Frontend Studio (`frontend/index.html`)**: Self-contained interactive web application that runs directly in any modern browser, GitHub Pages, Vercel, or Netlify without external API keys or login walls.
2. **FastAPI Multi-Agent Backend (`backend/main.py`)**: Asynchronous Python orchestration engine (`asyncio.gather`) running the 4 governance agents concurrently with SHA-256 audit logging.

## 📦 Quick Deployment for Round 2 Submission Links
- **Deploy Working Project Link (1-Click)**:
  - **GitHub Pages**: Push this repository to GitHub → Settings → Pages → Deploy from `/frontend` (or root).
  - **Vercel / Netlify**: Drag and drop the `frontend/` folder onto Netlify Drop or run `npx vercel frontend/`.
- **Run Full Stack Locally**:
  ```bash
  pip install -r backend/requirements.txt
  uvicorn backend.main:app --reload --port 8000
  ```
