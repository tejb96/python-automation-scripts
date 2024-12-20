import os
from PIL import Image
import pytesseract
import yaml

# Load configuration from the YAML file
with open("pybot-config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

class bcolors:
    OK = '\033[92m'  # GREEN
    WARNING = '\033[93m'  # YELLOW
    FAIL = '\033[91m'  # RED
    RESET = '\033[0m'  # RESET COLOR

# Set the Tesseract executable path
tesseract_path = data[0]['Config']['tesseract_path']
pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, "tesseract")

# Set the TESSDATA_PREFIX to point to the directory containing tessdata
os.environ["TESSDATA_PREFIX"] = "/usr/share/tesseract-ocr/5/tessdata"

# Test Tesseract setup
try:
    im = Image.open("images/tynan_shop.png")
    text = pytesseract.image_to_string(im)
    print(bcolors.OK + "Testing Tesseract is configured: Passed |", text)
except Exception as e:
    print(bcolors.FAIL + "Error running Tesseract:", e)
    print(bcolors.FAIL + "Check the Tesseract path and the presence of tessdata directory.")
