from flask import Flask, render_template, request
import os
import subprocess
import shutil
import sys

app = Flask(__name__)

UPLOAD_MODEL = "uploads/model"
UPLOAD_STUDENT = "uploads/students"

os.makedirs(UPLOAD_MODEL, exist_ok=True)
os.makedirs(UPLOAD_STUDENT, exist_ok=True)
os.makedirs("results", exist_ok=True)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    try:
        # =========================
        # DELETE OLD DATA
        # =========================
        paths_to_remove = [
            "processed/model",
            "processed/students/student_1",
            "results/results.csv"
        ]

        for path in paths_to_remove:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)

        # =========================
        # RECREATE FOLDERS
        # =========================
        os.makedirs("processed/model/pages", exist_ok=True)
        os.makedirs("processed/model/text", exist_ok=True)
        os.makedirs("processed/students/student_1/pages", exist_ok=True)
        os.makedirs("processed/students/student_1/text", exist_ok=True)
        os.makedirs("results", exist_ok=True)

        # =========================
        # SAVE FILES
        # =========================
        model_file = request.files['model']
        student_file = request.files['student']

        model_path = os.path.join(UPLOAD_MODEL, "model_answer.pdf")
        student_path = os.path.join(UPLOAD_STUDENT, "student_1.pdf")

        model_file.save(model_path)
        student_file.save(student_path)

        print("✅ Fresh files uploaded")
        print("Using interpreter:", sys.executable)

        # =========================
        # RUN OCR (IMPORTANT FIX)
        # =========================
        subprocess.run(
            [sys.executable, "ocr_extract.py"],
            check=True
        )

        # =========================
        # RUN RESULT GENERATOR
        # =========================
        subprocess.run(
            [sys.executable, "result_generator.py"],
            check=True
        )

        # =========================
        # CHECK RESULT FILE
        # =========================
        result_file = "results/results.csv"

        if not os.path.exists(result_file):
            return """
            <h2>❌ Evaluation Failed</h2>
            <p>results.csv not created.</p>
            <br><a href="/">⬅ Go Back</a>
            """

        # =========================
        # READ RESULT
        # =========================
        with open(result_file, "r") as f:
            lines = f.readlines()

        if len(lines) < 2:
            return """
            <h2>❌ No Result Found</h2>
            <p>CSV file empty.</p>
            <br><a href="/">⬅ Go Back</a>
            """

        data = lines[1].strip().split(",")

        return f"""
        <h2>📊 Result</h2>
        <p><b>Student ID:</b> {data[0]}</p>
        <p><b>Marks:</b> {data[1]}</p>
        <p><b>Total:</b> {data[2]}</p>
        <p><b>Percentage:</b> {data[3]}%</p>
        <br><a href="/">⬅ Go Back</a>
        """

    except subprocess.CalledProcessError as e:
        return f"""
        <h2>❌ Processing Error</h2>
        <p>{str(e)}</p>
        <br><a href="/">⬅ Go Back</a>
        """

    except Exception as e:
        return f"""
        <h2>❌ Unexpected Error</h2>
        <p>{str(e)}</p>
        <br><a href="/">⬅ Go Back</a>
        """


if __name__ == '__main__':
    app.run(debug=True)