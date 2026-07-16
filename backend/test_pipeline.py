import os
import sys
import cv2
import numpy as np

# Thêm thư mục hiện tại vào python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import CLASS_NAMES
from app.services.yolo_detector import YOLODetector
from app.services.densenet_classifier import DenseNetClassifier
from app.services.gradcam_engine import GradCAMEngine
from app.utils.image_helper import crop_bounding_boxes, blend_all

def test_run():
    print("=== START PIPELINE TEST ===")
    
    # 1. Tạo ảnh test giả lập (ảnh màu nền da nhạt và 2 đốm màu tròn mô phỏng nốt ruồi)
    print("Creating simulated test image...")
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    img[:] = [180, 200, 240]  # Màu da BGR
    # Vẽ đốm tổn thương 1 (Màu đỏ/nâu)
    cv2.circle(img, (150, 150), 30, (50, 50, 150), -1)
    # Vẽ đốm tổn thương 2 (Màu đen/xám)
    cv2.circle(img, (280, 250), 20, (80, 80, 80), -1)
    
    # 2. Khởi tạo các services
    print("Initializing models...")
    detector = YOLODetector()
    classifier = DenseNetClassifier(pretrained=True)
    target_layer = classifier.model.features.norm5
    gradcam = GradCAMEngine(classifier.model, target_layer)
    
    # 3. Chạy phát hiện YOLOv8
    print("Running YOLOv8...")
    raw_bboxes = detector.detect_lesions(img)
    print(f"Detected {len(raw_bboxes)} bounding boxes (including fallbacks).")
    
    # 4. Crop ảnh con
    crops, refined_bboxes = crop_bounding_boxes(img, raw_bboxes)
    
    heatmaps = []
    labels = []
    
    # 5. Chạy phân loại DenseNet & Grad-CAM
    for i, (crop, box) in enumerate(zip(crops, refined_bboxes)):
        print(f"Analyzing lesion crop {i+1}...")
        pred_label, pred_conf, probs = classifier.classify(crop)
        print(f"  Classified as: {pred_label} with confidence {pred_conf:.2%}")
        labels.append(f"{pred_label} ({pred_conf:.2%})")
        
        # Grad-CAM
        target_class_idx = CLASS_NAMES.index(pred_label)
        input_tensor = classifier.preprocess(crop)
        heatmap = gradcam.generate_heatmap(input_tensor, target_class_idx)
        heatmaps.append(heatmap)
        
    # 6. Trộn kết quả và lưu ảnh đầu ra
    print("Blending heatmap and drawing bounding boxes...")
    output_img = blend_all(img, refined_bboxes, heatmaps, labels, alpha=0.5)
    
    # Tạo thư mục test_outputs và lưu ảnh kết quả
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_outputs")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "test_result.jpg")
    cv2.imwrite(output_path, output_img)
    
    print(f"Saved test output image to: {output_path}")
    print("=== PIPELINE TEST COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    test_run()
