import os
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from google.genai import types

# Initialize Flask app
app = Flask(__name__)

# Enable CORS to allow your GitHub Pages frontend to communicate with this Render backend
CORS(app)

# Initialize Google GenAI client
# Ensure the GEMMA_API_KEY is set in your Render Environment Variables
client = genai.Client(api_key=os.environ.get("GEMMA_API_KEY"))

# ----------------- COURSE DATA -----------------
# Keep this minimal to easily modify your rules
COURSES = [
    {"code": "CSL201", "name": "Discrete Mathematics", "category": "PC", "semester": 3, "branch": "CSE", "slot": "A"},
    {"code": "DSL201", "name": "Mathematical Foundations for Data Science", "category": "PC", "semester": 3, "branch": "DSAI", "slot": "B2"},
    {"code": "DSL504", "name": "Natural Language Processing", "category": "PE", "semester": "Elective", "branch": "DSAI", "slot": "M"},
    {"code": "CSL559", "name": "Computer Systems Design", "category": "PE", "semester": "Elective", "branch": "CSE", "slot": "K"},
    # You can add the rest of your courses here
]
# -----------------------------------------------

@app.route("/")
def index():
    # This route is optional if you are hosting the frontend on GitHub Pages,
    # but it's good to keep so Render has a default page to show.
    return render_template("index.html")

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.json
    
    # Deterministically filter courses before sending to Gemma
    mandatory = [c for c in COURSES if c.get("branch") == data["branch"] and str(c.get("semester")) == str(data["semester"])]
    electives = [c for c in COURSES if c.get("category") in ["PE", "OE"]]

    prompt = f"""
    You are an IIT Bhilai Academic Advisor. 
    Student Profile: Branch: {data['branch']}, Target Role: {data['dream_role']}, Interests: {data['interests']}.
    
    Mandatory Core Courses available: {json.dumps(mandatory)}
    Elective Courses available: {json.dumps(electives)}
    
    Task: Select all mandatory courses, and pick the 2 most relevant electives for their dream role.
    Ensure no slot conflicts. 
    Output strictly as JSON matching this schema:
    {{"mandatory": [{{"code": "...", "name": "...", "slot": "...", "reason": "..."}}], "electives": [{{"code": "...", "name": "...", "slot": "...", "reason": "..."}}], "strategy": "..."}}
    """

    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it", # Standard Gemma 4 model endpoint
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        return jsonify({"success": True, "data": json.loads(response.text)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Required for local testing, but Gunicorn will use the 'app' variable directly on Render
if __name__ == "__main__":
    app.run(debug=True, port=5000)        "ltpc": "2-1-2-4",
        "discipline": "CSE",
        "program": "BTech",
        "semester": 3,
        "category": "PC",
        "slot": "F12, F3",
        "tags": ["software", "algorithms", "systems"]
    },
    {
        "code": "CSP203",
        "name": "Software Tools & Technologies Lab",
        "ltpc": "1-0-4-3",
        "discipline": "CSE",
        "program": "BTech",
        "semester": 3,
        "category": "PC",
        "slot": "B1",
        "tags": ["devops", "linux", "tools", "docker"]
    },
    {
        "code": "DSL201",
        "name": "Mathematical Foundations for Data Science",
        "ltpc": "3-1-0-4",
        "discipline": "DSAI",
        "program": "BTech",
        "semester": 3,
        "category": "PC",
        "slot": "B2",
        "tags": ["data science", "linear algebra", "ai", "ml"]
    },
    {
        "code": "MAL403",
        "name": "Probability and Statistics",
        "ltpc": "3-1-0-4",
        "discipline": "MA",
        "program": "BTech",
        "semester": 3,
        "category": "PL",
        "slot": "B3",
        "tags": ["math", "data science", "statistics", "ai"]
    },
    # --- Electives (PE / OE) ---
    {
        "code": "DSL504",
        "name": "Natural Language Processing",
        "ltpc": "3-0-2-4",
        "discipline": "DSAI",
        "program": "BTech",
        "semester": "Elective",
        "category": "PE",
        "slot": "M",
        "tags": ["nlp", "ai", "llm", "transformers", "data science"]
    },
    {
        "code": "CSL622",
        "name": "Quantum Computing for Computer Scientists",
        "ltpc": "2-0-2-3",
        "discipline": "CSE",
        "program": "BTech",
        "semester": "Elective",
        "category": "PE",
        "slot": "L",
        "tags": ["quantum", "algorithms", "physics"]
    },
    {
        "code": "CSL559",
        "name": "Computer Systems Design",
        "ltpc": "3-0-2-4",
        "discipline": "CSE",
        "program": "BTech",
        "semester": "Elective",
        "category": "PE",
        "slot": "K",
        "tags": ["systems", "distributed systems", "backend", "architecture"]
    },
    {
        "code": "MML558",
        "name": "AI and ML for Materials Engineering",
        "ltpc": "3-0-0-3",
        "discipline": "MSME",
        "program": "BTech",
        "semester": "Elective",
        "category": "OE",
        "slot": "K",
        "tags": ["materials", "ai", "interdisciplinary"]
    }
]

# -----------------------------------------------

@app.route("/")
def index():
    # This route is optional if you are hosting the frontend on GitHub Pages,
    # but it's good to keep so Render has a default page to show.
    return render_template("index.html")

@app.route("/api/recommend", methods=["POST"])
def recommend():
    data = request.json
    
    # Deterministically filter courses before sending to Gemma
    mandatory = [c for c in COURSES if c.get("branch") == data["branch"] and str(c.get("semester")) == str(data["semester"])]
    electives = [c for c in COURSES if c.get("category") in ["PE", "OE"]]

    prompt = f"""
    You are an IIT Bhilai Academic Advisor. 
    Student Profile: Branch: {data['branch']}, Target Role: {data['dream_role']}, Interests: {data['interests']}.
    
    Mandatory Core Courses available: {json.dumps(mandatory)}
    Elective Courses available: {json.dumps(electives)}
    
    Task: Select all mandatory courses, and pick the 2 most relevant electives for their dream role.
    Ensure no slot conflicts. 
    Output strictly as JSON matching this schema:
    {{"mandatory": [{{"code": "...", "name": "...", "slot": "...", "reason": "..."}}], "electives": [{{"code": "...", "name": "...", "slot": "...", "reason": "..."}}], "strategy": "..."}}
    """

    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it", # Standard Gemma 4 model endpoint
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.2
            )
        )
        return jsonify({"success": True, "data": json.loads(response.text)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Required for local testing, but Gunicorn will use the 'app' variable directly on Render
if __name__ == "__main__":
    app.run(debug=True, port=5000)    {
        "code": "DSL201",
        "name": "Mathematical Foundations for Data Science",
        "ltpc": "3-1-0-4",
        "discipline": "DSAI",
        "program": "BTech",
        "semester": 3,
        "category": "PC",
        "slot": "B2",
        "tags": ["data science", "linear algebra", "ai", "ml"]
    },
    {
        "code": "MAL403",
        "name": "Probability and Statistics",
        "ltpc": "3-1-0-4",
        "discipline": "MA",
        "program": "BTech",
        "semester": 3,
        "category": "PL",
        "slot": "B3",
        "tags": ["math", "data science", "statistics", "ai"]
    },
    # --- Electives (PE / OE) ---
    {
        "code": "DSL504",
        "name": "Natural Language Processing",
        "ltpc": "3-0-2-4",
        "discipline": "DSAI",
        "program": "BTech",
        "semester": "Elective",
        "category": "PE",
        "slot": "M",
        "tags": ["nlp", "ai", "llm", "transformers", "data science"]
    },
    {
        "code": "CSL622",
        "name": "Quantum Computing for Computer Scientists",
        "ltpc": "2-0-2-3",
        "discipline": "CSE",
        "program": "BTech",
        "semester": "Elective",
        "category": "PE",
        "slot": "L",
        "tags": ["quantum", "algorithms", "physics"]
    },
    {
        "code": "CSL559",
        "name": "Computer Systems Design",
        "ltpc": "3-0-2-4",
        "discipline": "CSE",
        "program": "BTech",
        "semester": "Elective",
        "category": "PE",
        "slot": "K",
        "tags": ["systems", "distributed systems", "backend", "architecture"]
    },
    {
        "code": "MML558",
        "name": "AI and ML for Materials Engineering",
        "ltpc": "3-0-0-3",
        "discipline": "MSME",
        "program": "BTech",
        "semester": "Elective",
        "category": "OE",
        "slot": "K",
        "tags": ["materials", "ai", "interdisciplinary"]
    }
]
