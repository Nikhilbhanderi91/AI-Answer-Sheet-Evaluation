from paddleocr import PaddleOCR
import os
from pdf2image import convert_from_path
import sys

# Get student name
if len(sys.argv) > 1:
    student_name = sys.argv[1]
else:
    student_name = "student_1"

# Paths
model_pdf = "uploads/model/model_answer.pdf"
student_pdf = f"uploads/students/{student_name}.pdf"

model_pages_dir = "processed/model/pages"
student_pages_dir = f"processed/students/{student_name}/pages"

model_text_path = "processed/model/text/model.txt"
student_text_path = f"processed/students/{student_name}/text/student.txt"

# Create folders
os.makedirs(model_pages_dir, exist_ok=True)
os.makedirs(student_pages_dir, exist_ok=True)
os.makedirs("processed/model/text", exist_ok=True)
os.makedirs(f"processed/students/{student_name}/text", exist_ok=True)

# Convert PDF → images
model_pages = convert_from_path(model_pdf, dpi=300)
for i, page in enumerate(model_pages):
    page.save(f"{model_pages_dir}/model_{i}.jpg", "JPEG")

student_pages = convert_from_path(student_pdf, dpi=300)
for i, page in enumerate(student_pages):
    page.save(f"{student_pages_dir}/student_{i}.jpg", "JPEG")

# Initialize OCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# OCR function
def extract_text(folder):
    full_text = ""
    for img in sorted(os.listdir(folder)):
        path = os.path.join(folder, img)

        result = ocr.ocr(path)

        for line in result:
            full_text += line[1][0] + "\n"

    return full_text

# Extract
model_text = extract_text(model_pages_dir)
student_text = extract_text(student_pages_dir)

# Save
with open(model_text_path, "w") as f:
    f.write(model_text)

with open(student_text_path, "w") as f:
    f.write(student_text)

print("✅ PaddleOCR Done")