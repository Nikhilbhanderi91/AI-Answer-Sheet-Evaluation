import easyocr
import numpy as np

# -----------------------
# 🔥 Initialize EasyOCR Reader (runs once)
# -----------------------
# gpu=False → recommended for Mac (MPS not fully supported)
reader = easyocr.Reader(['en'], gpu=False)


# -----------------------
# 🔥 Extract Text Function
# -----------------------
def extract_text(image):
    """
    Extract text from image using EasyOCR with improved settings
    """

    # 🔥 Convert PIL image → numpy array (VERY IMPORTANT)
    if not isinstance(image, np.ndarray):
        image = np.array(image)

    # -----------------------
    # 🔥 Improved OCR detection settings
    # -----------------------
    result = reader.readtext(
        image,
        detail=0,              # return only text
        paragraph=True,        # group nearby text (better structure)
        contrast_ths=0.5,      # helps low-contrast text
        adjust_contrast=0.7    # improves clarity
    )

    # -----------------------
    # 🔥 Join text with newline
    # -----------------------
    text = "\n".join(result)

    return text