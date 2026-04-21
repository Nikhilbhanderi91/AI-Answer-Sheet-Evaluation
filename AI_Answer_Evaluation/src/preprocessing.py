import cv2

def preprocess_image(image_path):
    img = cv2.imread(image_path)

    # 🔥 Safety check
    if img is None:
        raise ValueError("Image not found! Check path.")

    # -----------------------
    # Step 1: Convert to grayscale
    # -----------------------
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # -----------------------
    # 🔥 Step 2: Increase contrast (VERY IMPORTANT)
    # -----------------------
    gray = cv2.convertScaleAbs(gray, alpha=1.5, beta=0)

    # -----------------------
    # Step 3: Remove noise
    # -----------------------
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # -----------------------
    # 🔥 Step 4: Adaptive Threshold (BEST for OCR)
    # -----------------------
    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return thresh