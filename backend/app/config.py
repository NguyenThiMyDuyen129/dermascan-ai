import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# Model configurations
YOLO_MODEL_PATH = os.path.join(BASE_DIR, "weights", "yolov8_best.pt")
# Fallback sang model mặc định nếu chưa tải model train từ Colab
if not os.path.exists(YOLO_MODEL_PATH):
    YOLO_MODEL_PATH = "yolov8n.pt"

DENSENET_MODEL_NAME = "densenet121"
DENSENET_WEIGHTS_PATH = os.path.join(BASE_DIR, "weights", "densenet.pth")

# Danh sách nhãn phân loại da
CLASS_NAMES = ["Benign", "Malignant", "Inflammatory"]
