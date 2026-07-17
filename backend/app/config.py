import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")

# Tên mô hình chính xác trên đĩa
YOLO_MODEL_PATH = os.path.join(BASE_DIR, "weights", "yolo_best.pt")
# Fallback sang model mặc định nếu chưa tải model train từ Colab
if not os.path.exists(YOLO_MODEL_PATH):
    YOLO_MODEL_PATH = "yolov8n.pt"

DENSENET_MODEL_NAME = "densenet121"
DENSENET_WEIGHTS_PATH = os.path.join(BASE_DIR, "weights", "best_densenet.pth")

# 7 lớp tổn thương da của bộ dữ liệu HAM10000
CLASS_NAMES = ["akiec", "bcc", "bkl", "df", "mel", "nv", "vasc"]

# Ánh xạ tên viết tắt sang tên y khoa đầy đủ bằng tiếng Việt để hiển thị trực quan
CLASS_MAP = {
    "akiec": "Dày sừng quang hóa (AKIEC)",
    "bcc": "Ung thư biểu mô tế bào đáy (BCC)",
    "bkl": "Dày sừng lành tính (BKL)",
    "df": "U sợi da (DF)",
    "mel": "Ung thư hắc tố Melanoma (MEL)",
    "nv": "Nốt ruồi hắc tố (NV)",
    "vasc": "Tổn thương mạch máu (VASC)"
}

# Tham số tối ưu hóa mô hình YOLOv8 (Phương án 1)
YOLO_CONF_THRESHOLD = 0.25  # Khôi phục về ngưỡng mặc định để tránh False Positive
YOLO_BBOX_PADDING = 0.0     # Khôi phục về 0.0 để giữ nguyên BBox sát thực tế của YOLOv8
