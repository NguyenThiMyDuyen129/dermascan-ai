import os
import sys
import cv2
import numpy as np
import gradio as gr
import torch

# Thêm thư mục hiện tại vào python path để import từ backend
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from backend.app.config import CLASS_NAMES
from backend.app.services.yolo_detector import YOLODetector
from backend.app.services.densenet_classifier import DenseNetClassifier
from backend.app.services.gradcam_engine import GradCAMEngine
from backend.app.utils.image_helper import crop_bounding_boxes, blend_all

# Khởi tạo các mô hình AI toàn cục
print("=== ĐANG TẢI CÁC MÔ HÌNH AI ===")
detector = YOLODetector()
classifier = DenseNetClassifier(pretrained=True)
target_layer = classifier.model.features.norm5
gradcam = GradCAMEngine(classifier.model, target_layer)
print("=== TẢI MÔ HÌNH THÀNH CÔNG ===")

def process_pipeline(image):
    if image is None:
        return [], [], []
    
    # Gradio nhận ảnh dạng RGB (numpy array), chuyển sang BGR để OpenCV xử lý
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    # Giai đoạn 1: Tìm vùng tổn thương bằng YOLOv8
    raw_bboxes = detector.detect_lesions(img_bgr)
    crops, refined_bboxes = crop_bounding_boxes(img_bgr, raw_bboxes)
    
    heatmaps = []
    labels = []
    
    # Giai đoạn 2: Phân loại và sinh Grad-CAM cho từng ảnh con
    for crop, box in zip(crops, refined_bboxes):
        pred_label, pred_conf, _ = classifier.classify(crop)
        labels.append(f"{pred_label} ({pred_conf:.2%})")
        
        target_class_idx = CLASS_NAMES.index(pred_label)
        input_tensor = classifier.preprocess(crop)
        
        # Tạo bản đồ nhiệt
        heatmap = gradcam.generate_heatmap(input_tensor, target_class_idx)
        heatmaps.append(heatmap)
        
    return refined_bboxes, heatmaps, labels

def analyze_and_render(image, alpha):
    if image is None:
        return None, [], [], [], "Vui lòng tải ảnh lên trước!"
    
    # Chạy pipeline phân tích
    bboxes, heatmaps, labels = process_pipeline(image)
    
    if not bboxes:
        return image, [], [], [], "Không phát hiện tổn thương nào trên da."
    
    # Trộn ảnh gốc và heatmap
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    blended_bgr = blend_all(img_bgr, bboxes, heatmaps, labels, alpha)
    blended_rgb = cv2.cvtColor(blended_bgr, cv2.COLOR_BGR2RGB)
    
    summary = "\n".join([f"- Vùng {i+1}: {lbl}" for i, lbl in enumerate(labels)])
    log_text = f"Đã phát hiện {len(bboxes)} vùng tổn thương:\n{summary}"
    
    return blended_rgb, bboxes, heatmaps, labels, log_text

def update_opacity(image, bboxes, heatmaps, labels, alpha):
    # Nếu chưa chạy phân tích hoặc không có bboxes, trả về ảnh gốc
    if image is None or not bboxes:
        return image
        
    img_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    blended_bgr = blend_all(img_bgr, bboxes, heatmaps, labels, alpha)
    blended_rgb = cv2.cvtColor(blended_bgr, cv2.COLOR_BGR2RGB)
    return blended_rgb

# Xây dựng giao diện Web bằng Gradio Blocks
with gr.Blocks(theme=gr.themes.Soft(), css="footer {visibility: hidden}") as demo:
    gr.Markdown(
        """
        # 🩺 DermaScan AI - Skin Lesion Localization & Explainability
        ### Hệ thống Phân tích, Khoanh vùng & Giải thích Tổn thương Da
        *Quy trình Two-Stage chuyên nghiệp: YOLOv8 phát hiện tổn thương + DenseNet phân loại & Grad-CAM chỉ ra đặc trưng quyết định.*
        """
    )
    
    # Bộ lưu trữ State cục bộ để tối ưu hóa slider không cần predict lại
    state_bboxes = gr.State([])
    state_heatmaps = gr.State([])
    state_labels = gr.State([])
    
    with gr.Row():
        with gr.Column(scale=1):
            # Input: Tải ảnh lên
            input_image = gr.Image(label="Ảnh vùng da cần kiểm tra", type="numpy")
            
            # Slider thay đổi độ mờ (Opacity)
            opacity_slider = gr.Slider(
                minimum=0.0, 
                maximum=1.0, 
                value=0.5, 
                step=0.05, 
                label="Độ mờ Bản đồ nhiệt (Heatmap Opacity)"
            )
            
            # Nút bấm chạy phân tích
            btn_analyze = gr.Button("Phân tích Tổn thương Da", variant="primary")
            
        with gr.Column(scale=1):
            # Output: Hiển thị kết quả ảnh
            output_image = gr.Image(label="Kết quả Phân tích (Heatmap & Bounding Box)")
            
            # Bảng thông tin chuẩn đoán
            diagnostic_log = gr.Textbox(label="Kết quả chẩn đoán chi tiết", interactive=False, lines=4)

    # Đăng ký sự kiện phân tích chính
    btn_analyze.click(
        fn=analyze_and_render,
        inputs=[input_image, opacity_slider],
        outputs=[output_image, state_bboxes, state_heatmaps, state_labels, diagnostic_log]
    )
    
    # Đăng ký sự kiện kéo thanh trượt (Cực mượt do lấy dữ liệu từ State đã tính sẵn)
    opacity_slider.change(
        fn=update_opacity,
        inputs=[input_image, state_bboxes, state_heatmaps, state_labels, opacity_slider],
        outputs=output_image
    )

if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)
