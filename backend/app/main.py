import io
import base64
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import CLASS_NAMES
from .services.yolo_detector import YOLODetector
from .services.densenet_classifier import DenseNetClassifier
from .services.gradcam_engine import GradCAMEngine
from .utils.image_helper import crop_bounding_boxes, blend_all

app = FastAPI(title="DermaScan AI API")

# Cấu hình CORS để React Frontend có thể gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo các services (Load models khi khởi động server)
detector = None
classifier = None
gradcam = None

@app.on_event("startup")
def load_models():
    global detector, classifier, gradcam
    print("Loading YOLOv8 Detector...")
    detector = YOLODetector()
    
    print("Loading DenseNet Classifier...")
    classifier = DenseNetClassifier(pretrained=True)
    
    print("Initializing Grad-CAM Engine...")
    # Lấy layer convolutional cuối cùng của DenseNet121
    target_layer = classifier.model.features.norm5
    gradcam = GradCAMEngine(classifier.model, target_layer)
    print("All models loaded successfully!")

class LesionResponse(BaseModel):
    bbox: list  # [x1, y1, x2, y2]
    label: str
    confidence: float
    heatmap_b64: str  # Heatmap ảnh dạng base64 để frontend tự vẽ đè

class AnalysisResponse(BaseModel):
    original_b64: str
    annotated_b64: str  # Ảnh đã vẽ sẵn box + heatmap với mặc định alpha
    lesions: list[LesionResponse]

def numpy_to_b64(img: np.ndarray, format: str = ".jpg"):
    _, buffer = cv2.imencode(format, img)
    return base64.b64encode(buffer).decode("utf-8")

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    alpha: float = Query(0.5, ge=0.0, le=1.0)
):
    # 1. Đọc ảnh từ request
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Sao lưu ảnh gốc để chuyển đổi base64
    original_b64 = numpy_to_b64(img)

    # 2. Bước 1: Phát hiện Bounding Box bằng YOLOv8
    raw_bboxes = detector.detect_lesions(img)
    
    # Cắt ảnh con theo bboxes
    crops, refined_bboxes = crop_bounding_boxes(img, raw_bboxes)
    
    lesions_data = []
    heatmaps = []
    labels = []

    # 3. Bước 2: Phân loại và tính Grad-CAM trên từng ảnh crop
    for crop, box in zip(crops, refined_bboxes):
        # Phân loại bằng DenseNet
        pred_label, pred_conf, probs = classifier.classify(crop)
        labels.append(f"{pred_label} ({pred_conf:.2%})")
        
        # Tính Grad-CAM cho class được dự đoán
        target_class_idx = CLASS_NAMES.index(pred_label)
        input_tensor = classifier.preprocess(crop)
        
        # Sinh heatmap (kích thước [H, W], giá trị từ 0.0 -> 1.0)
        heatmap = gradcam.generate_heatmap(input_tensor, target_class_idx)
        heatmaps.append(heatmap)
        
        # Chuyển đổi heatmap thô thành ảnh màu đen trắng base64 để truyền về client
        heatmap_uint8 = np.uint8(255 * heatmap)
        # Thay đổi kích thước heatmap về bằng kích thước crop
        heatmap_resized = cv2.resize(heatmap_uint8, (crop.shape[1], crop.shape[0]))
        heatmap_b64 = numpy_to_b64(heatmap_resized)
        
        lesions_data.append(LesionResponse(
            bbox=box[:4],
            label=pred_label,
            confidence=pred_conf,
            heatmap_b64=heatmap_b64
        ))

    # 4. Trộn ảnh kết quả mặc định ở phía backend
    annotated_img = blend_all(img, refined_bboxes, heatmaps, labels, alpha)
    annotated_b64 = numpy_to_b64(annotated_img)

    return AnalysisResponse(
        original_b64=original_b64,
        annotated_b64=annotated_b64,
        lesions=lesions_data
    )
