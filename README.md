# career_planner
# Career Roadmapper

**Start from the job you want, then work backwards to where you are today.**

Built for **Ideathon 2.0 - Code2Career AI Hackathon** (Problem Statement 1: Reverse-Engineered Career Roadmapper).

**Live demo:** [paste your Render link here]

## The problem

Most career roadmaps start with "learn Python" and hope it leads to a job. Students don't know which skills a specific role needs, how far they are from it, or how to fit the learning into the time they have.

## Our approach: reverse engineering

1. The user enters their current skills and a target job role. They can also paste a real job posting.
2. The AI first works out what the job needs.
3. It then compares those requirements with what the user already knows.
4. Finally it builds a week-by-week plan that fits the user's available time.

## Features

- **Skill match percentage** for each skill, plus an overall readiness score
- **Radar chart** comparing "you today" with "what the job needs"
- **Adjustable time period** (1-8 weeks) and daily study hours, set with sliders
- **Job posting input** so the plan is based on a real employer's requirements
- **Reverse view** that flips the plan to show the goal first and today last
- **Task checklist** with progress tracking (saved in the browser)
- **Download** the plan as a text file and **print** it as a clean page
- Project ideas and interview questions for the chosen role
- Dark and light mode, mobile-friendly layout
- **Fallback plan**: if the AI service is busy, the app shows a sample plan instead of an error page

## Tech stack

| Part | Technology |
|---|---|
| Backend | Python, Flask |
| AI | Google Gemini API (`google-genai`) |
| Frontend | HTML, CSS, JavaScript (no framework) |
| Hosting | Render, served with gunicorn |

## How it works

The Flask backend sends a structured prompt to Gemini and asks for JSON only. The backend then validates and cleans the response (clamps numbers, checks priorities, limits list sizes) and calculates the skill-match and readiness percentages itself. The frontend draws the results: charts, timeline, checklist and buttons.

## Run it locally

1. Clone the repo and open the folder.
2. Install the libraries:
```
   pip install -r requirements.txt
```
3. Set your Gemini API key (get one at https://aistudio.google.com/apikey).

   Windows PowerShell:
```
   $env:GEMINI_API_KEY="your-key"
```
   Mac / Linux:
```
   export GEMINI_API_KEY="your-key"
```
4. Start the app:
```
   python app.py
```
5. Open http://127.0.0.1:5000

The API key is read from an environment variable. It is never stored in the code or in this repository.

## Deployment

Deployed on Render as a Web Service.

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn app:app --timeout 120`
- Environment variables: `GEMINI_API_KEY`, `PYTHON_VERSION`

## Project structure

```
career_planner/
  app.py            Flask backend, AI prompt, and the web page
  requirements.txt  Python dependencies
  list_models.py    Helper to list the Gemini models available to a key
  README.md         This file
```

## Limitations and future scope

- Skill levels are AI estimates based on what the user types, not a tested assessment.
- Progress is stored in the browser only, so it does not sync between devices.
- Future ideas: resume upload, adaptive plans that re-plan as tasks are completed, a mock interview mode, and links to verified free courses.

## Team

[Your name], BCA, [your college] - solo participant