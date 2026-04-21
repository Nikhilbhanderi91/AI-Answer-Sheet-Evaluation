from flask import Flask, render_template, request
import os
import subprocess
import shutil

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

UPLOAD_MODEL = "uploads/model"
UPLOAD_STUDENT = "uploads/students"

os.makedirs(UPLOAD_MODEL, exist_ok=True)
os.makedirs(UPLOAD_STUDENT, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    model_file = request.files['model']
    student_file = request.files['student']

    model_path = os.path.join(UPLOAD_MODEL, "model_answer.pdf")
    model_file.save(model_path)

    student_filename = student_file.filename
    student_name = student_filename.split(".")[0]

    student_path = os.path.join(UPLOAD_STUDENT, student_filename)
    student_file.save(student_path)

    print("Student Name:", student_name)
    print("Files uploaded")

    shutil.rmtree("processed/model/pages", ignore_errors=True)
    shutil.rmtree("processed/students", ignore_errors=True)

    if os.path.exists("processed/model/text/model.txt"):
        os.remove("processed/model/text/model.txt")

    if os.path.exists("results/results.csv"):
        os.remove("results/results.csv")

    print("Running OCR...")
    subprocess.run(
        ["python", "ocr_advanced.py", student_name],
        check=True
    )

    print("Running Evaluation...")
    subprocess.run(
        ["python", "result_generator.py", student_name],
        check=True
    )

    with open("results/results.csv", "r") as f:
        lines = f.readlines()
        last_line = lines[-1]

    data = last_line.strip().split(",")

    print("Cleaning old data...")

    shutil.rmtree("processed/model/pages", ignore_errors=True)
    shutil.rmtree("processed/students", ignore_errors=True)

    if os.path.exists("processed/model/text/model.txt"):
        os.remove("processed/model/text/model.txt")

    return f"""
    <h2>Result</h2>
    <p><b>Student ID:</b> {student_name}</p>
    <p><b>Marks:</b> {data[1]}</p>
    <p><b>Total:</b> {data[2]}</p>
    <p><b>Percentage:</b> {data[3]}%</p>
    <br><a href="/">Go Back</a>
    """

if __name__ == '__main__':
    app.run(debug=True)