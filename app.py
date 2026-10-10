import os
import pandas as pd
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure your API Key (Set this in your Render environment variables)
# If Gemma 4.0 is available via Vertex/Studio, replace the model name below. 
# Here we use 'gemini-1.5-flash' as the placeholder for the generative model.
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_DEFAULT_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

DATABASE_FILE = "PathFinder Database.xlsx"

def get_available_courses(branch, sem):
    """Fetch courses for the given branch and semester from the Excel database."""
    try:
        # The sheet names in the DB match the branches (e.g., 'CSE', 'DSAI')
        df = pd.read_excel(DATABASE_FILE, sheet_name=branch)
        # Filter by semester
        sem_courses = df[df['Sem'] == int(sem)]
        
        course_list = []
        for index, row in sem_courses.iterrows():
            course_list.append(f"{row['Course Code']}: {row['Course Name']} ({row['Credits']} Credits) - {row['Category']}")
        return "\n".join(course_list)
    except Exception as e:
        print(f"Database error: {e}")
        return "Course data unavailable for this selection."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    year = data.get('year')
    semester = data.get('semester')
    branch = data.get('branch')
    job_roles = data.get('job_roles', [])
    
    # 1. Fetch available courses for this specific branch and semester
    available_courses = get_available_courses(branch, semester)
    
    # 2. Build the prompt for Gemma
    prompt = f"""
    You are an academic advisor for IIT Bhilai. A {year} Year student in the {branch} branch 
    (Semester {semester}) is registering for courses. 
    
    Their career interests include: {', '.join(job_roles)}.
    
    Here is the list of courses available to them this semester based on the curriculum:
    {available_courses}
    
    Based on their career goals, recommend the best combination of these courses for this semester. 
    Explain why this combination is ideal for their chosen job roles. Keep the tone encouraging and professional.
    """
    
    # 3. Call the AI Model
    try:
        # Replace with your specific Gemma endpoint if using Vertex AI, 
        # or use standard Gemini models available via the API
        model = genai.GenerativeModel('gemini-1.5-flash') 
        response = model.generate_content(prompt)
        return jsonify({"recommendation": response.text})
    except Exception as e:
        return jsonify({"recommendation": f"Error generating recommendation: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))    """

    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it", 
            contents=prompt,
            config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2)
        )
        return jsonify({"success": True, "data": json.loads(response.text)})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)    data = request.json
    
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
