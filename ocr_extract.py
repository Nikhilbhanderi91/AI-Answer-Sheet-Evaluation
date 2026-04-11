from pdf2image import convert_from_path
import pytesseract
import cv2
import os
import sys

# ==========================================================
# TESSERACT PATH (WINDOWS)
# Uncomment if Tesseract not detected automatically
# ==========================================================
pytesseract.pytesseract.tesseract_cmd = \
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ==========================================================
# POPPLER PATH (YOUR INSTALLED LOCATION)
# ==========================================================
POPPLER_PATH = r"C:\Users\saval\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"

# ==========================================================
# FILE PATHS
# ==========================================================
model_pdf = "uploads/model/model_answer.pdf"
student_pdf = "uploads/students/student_1.pdf"

model_pages_dir = "processed/model/pages"
student_pages_dir = "processed/students/student_1/pages"

model_text_path = "processed/model/text/model.txt"
student_text_path = "processed/students/student_1/text/student.txt"

# ==========================================================
# CREATE REQUIRED FOLDERS
# ==========================================================
os.makedirs(model_pages_dir, exist_ok=True)
os.makedirs(student_pages_dir, exist_ok=True)
os.makedirs("processed/model/text", exist_ok=True)
os.makedirs("processed/students/student_1/text", exist_ok=True)

# ==========================================================
# CHECK POPPLER
# ==========================================================
if not os.path.exists(POPPLER_PATH):
    print("\n❌ POPPLER NOT FOUND")
    print("Expected path:")
    print(POPPLER_PATH)
    sys.exit(1)

# ==========================================================
# CHECK PDF FILES
# ==========================================================
if not os.path.exists(model_pdf):
    print(f"❌ Model PDF not found: {model_pdf}")
    sys.exit(1)

if not os.path.exists(student_pdf):
    print(f"❌ Student PDF not found: {student_pdf}")
    sys.exit(1)

# ==========================================================
# PDF -> IMAGE FUNCTION
# ==========================================================
def pdf_to_images(pdf_path, save_dir, prefix):
    try:
        pages = convert_from_path(
            pdf_path,
            dpi=400,
            poppler_path=POPPLER_PATH
        )

        if not pages:
            print(f"❌ No pages detected in {pdf_path}")
            sys.exit(1)

        for i, page in enumerate(pages):
            img_path = os.path.join(
                save_dir,
                f"{prefix}_{i+1}.jpg"
            )
            page.save(img_path, "JPEG")

        print(f"✅ Converted PDF: {pdf_path}")

    except Exception as e:
        print(f"❌ PDF conversion failed: {pdf_path}")
        print("ERROR:", e)
        sys.exit(1)

# ==========================================================
# CONVERT PDFs
# ==========================================================
print("\n📄 Converting PDFs to images...")

pdf_to_images(model_pdf, model_pages_dir, "model_page")
pdf_to_images(student_pdf, student_pages_dir, "student_page")

print("✅ PDF conversion completed")

# ==========================================================
# OCR ANSWER REGION ONLY
# ==========================================================
def extract_answer_regions(folder_path):
    all_text = ""

    files = sorted(os.listdir(folder_path))

    if len(files) == 0:
        print(f"❌ No images inside: {folder_path}")
        sys.exit(1)

    for img_name in files:
        img_path = os.path.join(folder_path, img_name)

        img = cv2.imread(img_path)

        if img is None:
            print(f"⚠️ Failed reading image: {img_path}")
            continue

        h, w, _ = img.shape

        # ==================================================
        # RIGHT SIDE WHERE ANSWERS EXIST
        # ==================================================
        crop = img[:, int(w * 0.70):w]

        # ==================================================
        # PREPROCESS IMAGE
        # ==================================================
        gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        _, thresh = cv2.threshold(
            gray,
            170,
            255,
            cv2.THRESH_BINARY
        )

        # ==================================================
        # OCR CONFIG
        # ==================================================
        config = r'--oem 3 --psm 6'

        try:
            text = pytesseract.image_to_string(
                thresh,
                config=config
            )

            all_text += text + "\n"

        except Exception as e:
            print(f"❌ OCR failed: {img_path}")
            print("ERROR:", e)
            sys.exit(1)

    return all_text

# ==========================================================
# RUN OCR
# ==========================================================
print("\n🔍 Extracting handwritten answers...")

model_text = extract_answer_regions(model_pages_dir)
student_text = extract_answer_regions(student_pages_dir)

# ==========================================================
# SAVE TEXT OUTPUT
# ==========================================================
with open(model_text_path, "w", encoding="utf-8") as f:
    f.write(model_text)

with open(student_text_path, "w", encoding="utf-8") as f:
    f.write(student_text)

print("✅ OCR extraction finished successfully")

# ==========================================================
# DEBUG OUTPUT
# ==========================================================
print("\n📘 MODEL OCR SAMPLE:")
print(model_text[:300])

print("\n🧑 STUDENT OCR SAMPLE:")
print(student_text[:300])