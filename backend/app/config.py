import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# Model configurations
YOLO_MODEL_PATH = "yolov8n.pt"  # Tải tự động nếu chưa có
DENSENET_MODEL_NAME = "densenet121"

# Danh sách nhãn phân loại da
CLASS_NAMES = ["Benign", "Malignant", "Inflammatory"]
