import re


def clean_ocr_text(text):
    text = text.upper()

    text = text.replace("8", "B")
    text = text.replace("6", "G")
    text = text.replace("1", "I")
    text = text.replace("|", "I")
    text = text.replace("0", "O")

    text = text.replace("?", "")
    text = text.replace("+", "")
    text = text.replace("-", "")
    text = text.replace("~", "")

    return text


def extract_mcq_answers(text, is_model=False):
    answers = {}

    text = clean_ocr_text(text)
    lines = [line.strip() for line in text.split("\n") if line.strip()]


    if is_model:
        q_num = 1
        for line in lines:
            match = re.search(r'ANSWER\s*[:\-]?\s*([A-D])', line)
            if match:
                answers[f"Q{q_num}"] = match.group(1)
                q_num += 1
        return answers


    detected_answers = []

    for i in range(len(lines)):

        line = lines[i].strip()

        match1 = re.search(r'^\d+[\)\.\s]+([A-D])$', line)
        if match1:
            detected_answers.append(match1.group(1))
            continue


        if re.match(r'^\d+[\)\.]$', line):
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()

                if re.fullmatch(r'[A-D8]', next_line):
                    ans = next_line
                    if ans == '8':
                        ans = 'B'

                    detected_answers.append(ans)
            continue


        if re.fullmatch(r'\d+', line):
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()

                if re.fullmatch(r'[A-D8]', next_line):
                    ans = next_line
                    if ans == '8':
                        ans = 'B'

                    detected_answers.append(ans)


    filtered = []
    for ans in detected_answers:
        if not filtered or filtered[-1] != ans:
            filtered.append(ans)

    detected_answers = filtered[:28]

    print("RAW DETECTED:", detected_answers)

    for i, ans in enumerate(detected_answers):
        answers[f"Q{i+1}"] = ans

    return answers



def evaluate_mcq(student_answers, model_answers):
    score = 0

    min_len = min(len(student_answers), len(model_answers))

    for i in range(1, min_len + 1):
        q = f"Q{i}"
        if student_answers.get(q) == model_answers.get(q):
            score += 1

    return score, min_len