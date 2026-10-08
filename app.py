import os
import time

from flask import Flask, render_template_string, request
from google import genai

app = Flask(__name__)

# The key comes from the environment, so it never goes into GitHub

PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Career Roadmapper</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 750px; margin: 30px auto; padding: 0 15px; background: #f5f6fa; }
    h1 { text-align: center; }
    form { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
    label { display: block; margin-top: 12px; font-weight: bold; }
    input { width: 100%; padding: 10px; margin-top: 5px; box-sizing: border-box; font-size: 16px; }
    button { margin-top: 18px; padding: 12px; width: 100%; font-size: 16px; background: #4a6cf7; color: white; border: none; border-radius: 6px; cursor: pointer; }
    .result { background: white; padding: 20px; margin-top: 20px; border-radius: 10px; white-space: pre-wrap; line-height: 1.5; }
    .error { color: #b00020; }
  </style>
</head>
<body>
  <h1>Career Roadmapper</h1>
  <form method="post" onsubmit="document.getElementById('btn').innerText='Thinking... please wait'">
    <label>Your skills</label>
    <input name="skills" value="{{ skills }}" placeholder="e.g. Python, basic SQL" required>
    <label>Target job role</label>
    <input name="role" value="{{ role }}" placeholder="e.g. Data Analyst" required>
    <button id="btn" type="submit">Get my plan</button>
  </form>

  {% if error %}
    <div class="result error">{{ error }}</div>
  {% elif plan %}
    <div class="result">{{ plan }}</div>
  {% endif %}
</body>
</html>
"""


from google.genai import types

client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=30000),  # give up after 30 seconds
)

MODELS = ["gemini-3.8-flash","gemini-3.6-flash","gemini-3.7-flash"]  # add other model names from list_models.py here


def ask_gemini(prompt):
    SAMPLE_PLAN = """(Live AI is busy, so this is a sample plan.)

Paste the Python / Data Analyst plan from Colab here."""
    last_error = None
    for model in MODELS:
        for attempt in range(3):
            try:
                response = client.models.generate_content(model=model, contents=prompt)
                return response.text, None
            except Exception as e:
                last_error = e
                time.sleep(2 * (attempt + 1))  # wait 2s, 4s, 6s
    return SAMPLE_PLAN, None
@app.route("/", methods=["GET", "POST"])
def home():
    skills = role = plan = error = ""
    if request.method == "POST":
        skills = request.form["skills"].strip()
        role = request.form["role"].strip()
        prompt = f"I know {skills}. I want to become a {role}. List 5 missing skills and a 2-week learning plan."
        plan, error = ask_gemini(prompt)
    return render_template_string(PAGE, skills=skills, role=role, plan=plan, error=error)


if __name__ == "__main__":
    app.run(debug=True)