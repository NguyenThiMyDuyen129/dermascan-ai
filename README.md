# 🩺 DermaScan AI - Skin Lesion Localization & Explainability

**DermaScan AI** là một hệ thống y tế số tiên tiến hỗ trợ chẩn đoán và phân tích tổn thương da sử dụng mô hình học sâu hai giai đoạn (Two-Stage / Cascade Architecture) kết hợp giải thích quyết định bằng bản đồ nhiệt (Grad-CAM). 

Hệ thống được thiết kế với giao diện Dashboard hiện đại phong cách công nghệ - y tế (Trắng - Cam - Xanh đậm) chạy trên nền tảng **Next.js (React)** kết hợp với **FastAPI (Python)**.

---

## 🚀 Các tính năng chính

1. **Phát hiện đa tổn thương (Stage 1 - YOLOv8)**: Tự động quét và định vị chính xác tất cả các vùng tổn thương da trên một bức ảnh (vẽ Bounding Box tương ứng).
2. **Phân loại chuyên sâu (Stage 2 - DenseNet121)**: Cắt (crop) từng vùng tổn thương phát hiện được từ Giai đoạn 1 và đưa qua DenseNet121 để phân loại bệnh lý chi tiết:
   - **Lành tính (Benign)**
   - **Ác tính (Malignant)**
   - **Viêm nhiễm (Inflammatory)**
3. **Bản đồ nhiệt giải thích (Grad-CAM Explainability)**: Trực quan hóa mức độ đóng góp của các vùng pixel da bằng bản đồ nhiệt màu sắc (Heatmap), giúp bác sĩ hiểu rõ tại sao AI đưa ra quyết định chẩn đoán.
4. **Điều khiển Opacity thời gian thực**: Thanh trượt độ mờ hoạt động mượt mà (<10ms) thông qua cơ chế lưu bộ nhớ đệm (caching) ở Frontend và xử lý trộn ảnh nhanh ở Backend.
5. **Nhật ký bệnh án (History Log)**: Lưu trữ các ca quét tổn thương da trong phiên làm việc để đối chiếu và xem lại nhanh.
6. **Hoạt động Offline 100%**: Sử dụng font chữ hệ thống mặc định, không cần tải font trực tuyến, ngăn ngừa tối đa lỗi hiển thị và giật lag giao diện.

---

## 🛠️ Kiến trúc Hệ thống

```
dermascan-ai/
├── backend/                      # Core Logic & API Service (FastAPI)
│   ├── app/
│   │   ├── main.py               # Các endpoints API (/api/analyze, /api/blend)
│   │   ├── config.py             # Cấu hình ngưỡng tin cậy, nhãn bệnh lý và đường dẫn
│   │   ├── services/
│   │   │   ├── yolo_detector.py  # Phát hiện vùng tổn thương da (YOLOv8)
│   │   │   ├── densenet_classifier.py # Phân loại bệnh lý (DenseNet121)
│   │   │   └── gradcam_engine.py      # Tạo bản đồ nhiệt Grad-CAM
│   │   └── utils/
│   │       └── image_helper.py   # Xử lý cắt ảnh, vẽ khung và trộn màu heatmap
│   ├── weights/                  # Thư mục lưu file model weights (.pt, .pth)
│   ├── requirements.txt          # Thư viện Python cần thiết
│   └── run.py                    # Khởi chạy FastAPI Server
│
├── frontend/                     # Giao diện Web Dashboard (Next.js)
│   ├── src/
│   │   ├── app/                  # Router & CSS cấu hình hệ thống
│   │   └── components/           # Components UI tái sử dụng (Uploader, ResultPanel,...)
│   ├── package.json              # Quản lý thư viện Node.js
│   └── next.config.js            # Cấu hình proxy chống lỗi CORS
│
└── .gitignore                    # Bảo mật dự án, loại trừ file weights và node_modules
```

---

## ⚙️ Hướng dẫn cài đặt & Khởi chạy

Dự án yêu cầu máy tính đã cài đặt **Python 3.9+** và **Node.js 18+**.

### Bước 1: Chuẩn bị file Model Weights (Trọng số mô hình)
Đặt các file trọng số của bạn vào thư mục `backend/weights/`:
- `yolov8_best.pt` (Mô hình YOLOv8 phát hiện tổn thương)
- `densenet.pth` (Mô hình DenseNet121 phân loại bệnh lý)
*(Lưu ý: Nếu chưa có file weights, hệ thống sẽ tự động sử dụng model pretrained mặc định từ COCO/ImageNet để chạy thử).*

### Bước 2: Khởi chạy Backend FastAPI (Cổng 8000)
Mở terminal và di chuyển vào thư mục `backend`:
```bash
cd backend

# 1. Tạo môi trường ảo (nếu chưa có)
python -m venv venv

# 2. Kích hoạt môi trường ảo (Chọn lệnh phù hợp với Terminal của bạn):
# - Dành cho PowerShell:
.\venv\Scripts\Activate.ps1
# - Dành cho Command Prompt (CMD):
venv\Scripts\activate
# - Dành cho Git Bash / Linux / macOS:
source venv/Scripts/activate

# 3. Cài đặt thư viện
pip install -r requirements.txt

# 4. Chạy backend
python run.py
```
*Server API hoạt động tại: `http://127.0.0.1:8000`*

### Bước 3: Khởi chạy Frontend Next.js (Cổng 3000)
Mở một terminal khác và di chuyển vào thư mục `frontend`:
```powershell
cd frontend
# Cài đặt các dependencies
npm install
# Chạy chế độ phát triển (dev)
npm run dev
```
*Giao diện Dashboard hoạt động tại: `http://localhost:3000`*

---

## 📝 Tài liệu Endpoints API chính

### 1. Phân tích hình ảnh: `POST /api/analyze`
- **Chức năng**: Tải ảnh thô lên, chạy qua pipeline 2 giai đoạn và trả về kết quả định vị kèm phân loại.
- **Tham số**:
  - `file`: Ảnh da cần quét (Multipart file)
  - `alpha`: Độ mờ mặc định ban đầu của heatmap (Mặc định: `0.5`)
- **Phản hồi mẫu**:
  ```json
  {
    "original_b64": "...",
    "annotated_b64": "...",
    "lesions": [
      {
        "bbox": [50, 60, 200, 250],
        "label": "Malignant",
        "confidence": 0.925,
        "heatmap_b64": "..."
      }
    ]
  }
  ```

### 2. Trộn màu nhanh: `POST /api/blend`
- **Chức năng**: Trộn nhanh ảnh gốc với các ảnh con heatmap và tọa độ có sẵn theo mức độ `alpha` mới.
- **Tham số (JSON Body)**:
  - `original_b64`: Ảnh gốc dạng base64
  - `bboxes`: Tọa độ các vùng phát hiện được
  - `heatmaps_b64`: Các bản đồ nhiệt thô (grayscale base64) của từng vùng
  - `labels`: Danh sách nhãn bệnh kèm tỷ lệ tin cậy
  - `alpha`: Độ mờ mới (`0.0` -> `1.0`)
- **Phản hồi**: Ảnh kết quả đã trộn dạng base64 (`blended_b64`).
