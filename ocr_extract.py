from pdf2image import convert_from_path
import pytesseract
import cv2
import os
import sys

if len(sys.argv) > 1:
    student_name = sys.argv[1]
else:
    student_name = "student_1"

model_pdf = "uploads/model/model_answer.pdf"
student_pdf = f"uploads/students/{student_name}.pdf"

model_pages_dir = "processed/model/pages"
student_pages_dir = f"processed/students/{student_name}/pages"

model_text_path = "processed/model/text/model.txt"
student_text_path = f"processed/students/{student_name}/text/student.txt"

os.makedirs(model_pages_dir, exist_ok=True)
os.makedirs(student_pages_dir, exist_ok=True)
os.makedirs("processed/model/text", exist_ok=True)
os.makedirs(f"processed/students/{student_name}/text", exist_ok=True)

print("Converting PDFs to images...")

model_pages = convert_from_path(model_pdf, dpi=300)
for i, page in enumerate(model_pages):
    page.save(f"{model_pages_dir}/model_page_{i+1}.jpg", "JPEG")

student_pages = convert_from_path(student_pdf, dpi=300)
for i, page in enumerate(student_pages):
    page.save(f"{student_pages_dir}/student_page_{i+1}.jpg", "JPEG")

print("Conversion done")

def extract_text_from_images(folder_path):
    full_text = ""
    
    for img_name in sorted(os.listdir(folder_path)):
        if img_name.startswith("."):
            continue
        
        img_path = os.path.join(folder_path, img_name)
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"Skipping: {img_path}")
            continue
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        
        text = pytesseract.image_to_string(thresh)
        full_text += text + "\n"
    
    return full_text

print("Extracting text...")

model_text = extract_text_from_images(model_pages_dir)
student_text = extract_text_from_images(student_pages_dir)

with open(model_text_path, "w") as f:
    f.write(model_text)

with open(student_text_path, "w") as f:
    f.write(student_text)

print("OCR completed and text saved")