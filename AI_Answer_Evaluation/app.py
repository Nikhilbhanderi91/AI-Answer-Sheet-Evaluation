import streamlit as st
from src.preprocessing import preprocess_image
from src.ocr import extract_text
from src.similarity import calculate_similarity
from src.evaluation import calculate_marks


def split_answers(text):
    answers = {}
    lines = text.split("\n")

    current_q = None
    current_ans = ""

    for line in lines:
        line = line.strip()

        if line.startswith("Q"):
            if current_q:
                answers[current_q] = current_ans.strip()

            current_q = line.split(":")[0]
            current_ans = line
        else:
            current_ans += " " + line

    if current_q:
        answers[current_q] = current_ans.strip()

    return answers


st.title("📄 AI Answer Sheet Evaluation System")

uploaded_file = st.file_uploader("Upload Answer Sheet", type=["jpg", "png"])

if uploaded_file:
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.read())

    st.image("temp.jpg", caption="Uploaded Answer Sheet")

    # Preprocess
    processed = preprocess_image("temp.jpg")

    # OCR
    student_text = extract_text(processed)

    # Load model answers
    with open("data/model_answers/model.txt", "r") as f:
        model_text = f.read()

    student_answers = split_answers(student_text)
    model_answers = split_answers(model_text)

    results = {}

    for q in model_answers:
        student_ans = student_answers.get(q, "")

        if student_ans == "":
            sim = 0
            marks = 0
        else:
            sim = calculate_similarity(student_ans, model_answers[q])
            marks = calculate_marks(sim)

        results[q] = {
            "similarity": round(sim, 2),
            "marks": marks
        }

    total_marks = sum([v["marks"] for v in results.values()])

    st.write("## Results")
    st.json(results)
    st.write("### Total Marks:", total_marks)