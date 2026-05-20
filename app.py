from flask import Flask, render_template_string, request
import os
from PyPDF2 import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_PAGE = """
<!DOCTYPE html>
<html>

<head>
    <title>AI Resume Analyzer</title>

    <style>

        body{
            font-family:Arial;
            background:linear-gradient(to right,#4facfe,#00f2fe);
            margin:0;
            padding:0;
        }

        .container{
            width:60%;
            margin:50px auto;
            background:white;
            padding:30px;
            border-radius:20px;
            text-align:center;
            box-shadow:0px 0px 20px gray;
        }

        h1{
            color:#2563eb;
        }

        .score{
            color:green;
            font-size:30px;
            font-weight:bold;
        }

        h2{
            color:purple;
        }

        h3{
            color:orange;
        }

        button{
            background:#2563eb;
            color:white;
            border:none;
            padding:12px 25px;
            border-radius:10px;
            cursor:pointer;
            font-size:18px;
        }

        button:hover{
            background:#1e40af;
        }

        ul{
            list-style:none;
            padding:0;
        }

        li{
            background:#f3f4f6;
            margin:10px;
            padding:12px;
            border-radius:10px;
            font-weight:bold;
        }

    </style>

</head>

<body>

<div class="container">

    <h1>AI Resume Analyzer</h1>

    <form action="/analyze" method="POST" enctype="multipart/form-data">

        <input type="file" name="resume" accept=".pdf" required>

        <br><br>

        <button type="submit">
            Upload & Analyze
        </button>

    </form>

    {% if analysis %}

        <p class="score">
            Resume Score: {{ score }}/100
        </p>

        <h2>
            Recommended Job Role: {{ job }}
        </h2>

        <h3>Detected Skills</h3>

        <ul>
        {% for skill in skills %}
            <li>{{ skill }}</li>
        {% endfor %}
        </ul>

        <h3>Suggestions</h3>

        <ul>
        {% for suggestion in suggestions %}
            <li>{{ suggestion }}</li>
        {% endfor %}
        </ul>

    {% endif %}

</div>

</body>
</html>
"""

SKILLS = [
    "python", "java", "flask", "html", "css",
    "sql", "machine learning", "ai",
    "data science", "pandas", "numpy",
    "javascript", "git"
]

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/analyze', methods=['POST'])
def analyze():

    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    text = ""

    reader = PdfReader(filepath)

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted

    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    score = len(found_skills) * 10

    if score > 100:
        score = 100

    suggestions = []

    if "flask" not in found_skills:
        suggestions.append("Add Flask projects")

    if "sql" not in found_skills:
        suggestions.append("Add SQL skill")

    if "git" not in found_skills:
        suggestions.append("Add GitHub projects")

    # Job Prediction

    if "python" in text and "flask" in text:
        job = "Python Backend Developer"

    elif "machine learning" in text or "ai" in text:
        job = "AI / Machine Learning Engineer"

    elif "html" in text and "css" in text:
        job = "Frontend Web Developer"

    elif "java" in text:
        job = "Java Developer"

    else:
        job = "Software Developer Fresher"

    return render_template_string(
        HTML_PAGE,
        analysis=True,
        score=score,
        skills=found_skills,
        suggestions=suggestions,
        job=job
    )

if __name__ == '__main__':
    app.run(debug=True)