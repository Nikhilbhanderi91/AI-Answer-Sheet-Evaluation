from flask import Flask, render_template, request
import os

app = Flask(__name__)

# Folders
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

    # Save uploaded files
    model_path = os.path.join(UPLOAD_MODEL, "model_answer.pdf")
    student_path = os.path.join(UPLOAD_STUDENT, "student_1.pdf")

    model_file.save(model_path)
    student_file.save(student_path)

    print("✅ Files uploaded")

    # 🔥 STEP 1: Run OCR
    print("🔄 Running OCR...")
    os.system("python ocr_extract.py")

    # 🔥 STEP 2: Run Evaluation
    print("🔄 Running Evaluation...")
    os.system("python result_generator.py")

    # 🔥 STEP 3: Read latest result
    with open("results/results.csv", "r") as f:
        lines = f.readlines()
        last_line = lines[-1]

    data = last_line.strip().split(",")

    return f"""
    <h2>📊 Result</h2>
    <p><b>Student ID:</b> {data[0]}</p>
    <p><b>Marks:</b> {data[1]}</p>
    <p><b>Total:</b> {data[2]}</p>
    <p><b>Percentage:</b> {data[3]}%</p>
    <br><a href="/">⬅ Go Back</a>
    """


if __name__ == '__main__':
    app.run(debug=True)