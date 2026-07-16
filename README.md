# DermaScan AI - Hệ thống Phân tích, Khoanh vùng & Giải thích Tổn thương Da

Hệ thống hỗ trợ bác sĩ và người dùng phân tích, phát hiện vị trí (Bounding Box) và phân loại các loại tổn thương da (Lành tính, Ác tính, Viêm nhiễm) kết hợp bản đồ nhiệt Grad-CAM để trực quan hóa vùng mô hình AI tập trung phân tích.

## Công nghệ sử dụng
- **Giai đoạn 1 (Detection):** YOLOv8 (Ultralytics) để phát hiện và khoanh vùng tổn thương da.
- **Giai đoạn 2 (Classification & Explainability):** DenseNet & Grad-CAM (PyTorch) để phân loại từng vùng tổn thương bị cắt ra và biểu diễn bản đồ nhiệt.
- **Giao diện:** Gradio (tiện lợi, có Opacity slider) và FastAPI + ReactJS.
