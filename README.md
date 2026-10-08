# ACEest Fitness & Gym – DevOps CI/CD

A Flask web application for gym management, delivered through an automated CI/CD workflow using Git, Pytest, Docker, Jenkins and GitHub Actions.

## API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| GET | `/programs` | List fitness programs |
| GET/POST | `/members` | List / register members |
| POST | `/bmi` | Calculate BMI (`weight` kg, `height` m) |

## Local Setup
```bash
git clone https://github.com/<username>/aceest-fitness-devops.git
cd aceest-fitness-devops
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py        # http://localhost:5000
```

## Running Tests Manually
```bash
python -m pytest                                  # local
docker build -t aceest-fitness .
docker run --rm aceest-fitness pytest             # inside container
```

## Run with Docker
```bash
docker build -t aceest-fitness .
docker run -d -p 5000:5000 aceest-fitness
```
The image uses `python:3.12-slim`, runs as a non-root user, disables pip cache and excludes non-runtime files via `.dockerignore`.

## CI/CD Overview
**GitHub Actions** (`.github/workflows/main.yml`) runs on every push and pull request:
1. **Build & Lint** – installs dependencies, runs flake8 syntax checks and compiles `app.py`.
2. **Docker Image Assembly** – builds the container image.
3. **Automated Testing** – runs the Pytest suite inside the container.

**Jenkins** (`Jenkinsfile`) acts as the secondary BUILD and quality gate. The job polls GitHub every 5 minutes, performs a clean checkout, creates a fresh virtual environment, lints, runs unit tests, builds the Docker image and runs tests inside it. The workspace is cleaned after each build.

## Branching Strategy
`main` (stable) ← `develop` (integration) ← `feature/*`, `infra/*`, `docs/*`, merged via pull requests.
