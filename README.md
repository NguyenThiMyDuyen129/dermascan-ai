# DermaScan AI - Skin Lesion Localization and Explainability Dashboard

DermaScan AI la mot he thong ho tro chan doan va phan tich ton thuong da su dung mo hinh hoc sau hai giai doan (Two-Stage Cascade Architecture) ket hop giai thich quyet dinh bang ban do nhiet do kich hoat (Grad-CAM Explainability). 

He thong duoc thiet ke voi giao dien Dashboard chay tren nen tang Next.js (React) ket hop voi FastAPI (Python) lam backend phuc vu tinh toan.

---

## Bo du lieu Huan luyen (HAM10000 Dataset)

He thong su dung mo hinh duoc huan luyen tren bo du lieu nghien cuu da lieu quoc te Skin Cancer MNIST: HAM10000. Cau truc cua bo du lieu bao gom cac tep tin sau:

*   HAM10000_images_part_1/: Thu muc chua phan thu nhat cua bo anh da lieu goc (dang anh mau JPEG co do phan giai goc cao).
*   HAM10000_images_part_2/: Thu muc chua phan thu hai cua bo anh da lieu goc.
*   HAM10000_metadata.csv: Tep chua thong tin thuoc tinh lam sang cua tung ca benh, bao gom:
    *   lesion_id: Ma dinh danh ca benh ton thuong.
    *   image_id: Ten file anh tuong ung.
    *   dx: Nhan chan doan benh ly viet tat (mel, nv, bcc, akiec, bkl, df, vasc).
    *   dx_type: Phuong phap xac thuc lam sang (chup cat lop, sinh thiet, y kien chuyen gia).
    *   age: Tuoi cua benh nhan.
    *   sex: Gioi tinh cua benh nhan.
    *   localization: Vi tri giai phau xuat hien ton thuong tren co the.
*   Tep nen bieu dien pixel muc thap:
    *   hmnist_28_28_L.csv: Tep du lieu anh muc xam (Grayscale) kich thuoc 28x28 pixel dang bang phang.
    *   hmnist_28_28_RGB.csv: Tep du lieu anh mau (RGB) kich thuoc 28x28 pixel dang bang phang.
    *   hmnist_8_8_L.csv: Tep du lieu anh muc xam kich thuoc 8x8 pixel dang bang phang.
    *   hmnist_8_8_RGB.csv: Tep du lieu anh mau kich thuoc 8x8 pixel dang bang phang.

---

## Huong dan Cap nhat Mo hinh sau khi Huan luyen tren Kaggle

Sau khi hoan thanh viec huan luyen mo hinh phat hien (YOLOv8) hoac mo hinh phan loai (DenseNet121) tren Kaggle, thuc hien quy trinh sau de tich hop trong so moi vao du an:

### Buoc 1: Tai tep trong so tu Kaggle
Tai xuong cac tep trong so dau ra cua phien huan luyen:
*   Mo hinh YOLOv8: Tai file trong so tot nhat best.pt.
*   Mo hinh DenseNet121: Tai file luu trong so mang tot nhat (.pth hoac .pt).

### Buoc 2: Di chuyen trong so vao thu muc du an
Sao chep va thay the cac tep tin trong so moi vao thu muc luu tru weights cua Backend:
*   Doi voi YOLOv8: Doi ten tep best.pt thanh yolo_best.pt va dat vao:
    d:\Project\XLA_dermascan-ai\backend\weights\yolo_best.pt
*   Doi voi DenseNet121: Dat file trong so phan loai (doi ten thanh best_densenet.pth) vao:
    d:\Project\XLA_dermascan-ai\backend\weights\best_densenet.pth

### Buoc 3: Chay kich ban don dep va chuan bi khong gian lam viec
Tai thu muc goc du an, hay chay lenh sau de tu dong don dep cac thu muc tam va doi ten cac file trong so mot cach an toan:
```bash
python backend/workspace_prep.py
```

### Buoc 4: Kiem tra Pipeline cuc bo bang Script
Chay script kiem tra ngoai tuyen de xac nhan cac trong so moi tuong thich tot voi ma nguon va khong gay ra loi xu ly hinh anh:
1. Kich hoat moi truong ao venv cua backend.
2. Chay tep tin kiem tra:
   ```bash
   python test_pipeline.py
   ```
Neu dau ra hien thi thong bao PIPELINE RUN COMPLETED SUCCESSFULLY WITHOUT ERRORS thi mo hinh moi da tuong thich hoan toan.

### Buoc 5: Khoi dong lai API Server
Tien hanh chay lai server FastAPI de he thong ap dung cac mo hinh moi:
```bash
python run.py
```

---

## Cong nghe Su dung (Tech Stack)

### 1. Backend
*   **FastAPI**: Framework Python dung de xay dung cac API endpoints nhan anh, xu ly pipeline AI va tra ket qua ve client.
*   **PyTorch**: Thu vien chay mo hinh phan loai DenseNet121 va thuc hien tinh toan ma tran Grad-CAM.
*   **Ultralytics YOLOv8**: Su dung de dinh vi vung ton thuong tren da (Bounding Box).
*   **OpenCV & NumPy**: Xu ly cat anh vung ton thuong, ve khung toa do, ap dung colormap JET cho ban do nhiet va tron anh (blend).
*   **Uvicorn**: ASGI web server chay backend Python.

### 2. Frontend
*   **Next.js (React & TypeScript)**: Framework xay dung giao dien Dashboard phia Client.
*   **Lucide React**: Thu vien icons hien thi tren giao dien.
*   **Vanilla CSS & Inline Styles**: Dinh dang phong cach giao dien ma khong phu thuoc vao thu vien CSS ben ngoai.

---

## Huong dan Cai dat & Khoi chay

### Buoc 1: Khoi chay Backend FastAPI (Cong 8000)
Mo terminal va di chuyen vao thu muc backend:
```bash
cd backend

# 1. Tao moi truong ao (venv) neu chua co
python -m venv venv

# 2. Kich hoat moi truong ao:
# - Windows PowerShell:
.\venv\Scripts\Activate.ps1
# - Windows Command Prompt (CMD):
venv\Scripts\activate
# - Git Bash / Linux / macOS:
source venv/Scripts/activate

# 3. Cai dat cac thu vien can thiet
pip install -r requirements.txt

# 4. Khoi chay server FastAPI
python run.py
```
API server hoat dong tai dia chi: http://127.0.0.1:8000

### Buoc 2: Khoi chay Frontend Next.js (Cong 3000)
Mo mot cua so terminal moi va di chuyen vao thu muc frontend:
```bash
cd frontend

# 1. Cai dat cac thu vien Node.js
npm install

# 2. Chay ung dung o che do phat trien
npm run dev
```
Giao dien Dashboard hoat dong tai dia chi: http://localhost:3000

---

## Cong viec Thuc hien & Phuong phap Trien khai

Duoi day la chi tiet cac hang muc cong viec da thuc hien va phuong phap xu ly ky thuat tuong ung qua cac giai doan phat trien cua du an:

| Giai doan | Cong viec thuc hien | Phuong phap trien khai & Chi tiet ky thuat |
| :--- | :--- | :--- |
| **Giai doan 1: Core Pipeline & Ket noi** | Phat hien ton thuong da (Stage 1) | Tich hop mo hinh YOLOv8 tai tu file trong so yolo_best.pt. Viet ma nguon trich xuat toa do Bounding Box, diem tin cay (confidence score) va chi so lop (class index) tu anh dau vao. |
| **Giai doan 1: Core Pipeline & Ket noi** | Phan loai benh ly da lieu (Stage 2) | Thiet lap tien xu ly: cat anh vung ton thuong dua tren toa do YOLOv8, chuan hoa kich thuoc ve 224x224, chuyen thanh Tensor va thuc hien chuan hoa du lieu theo ImageNet. Dua anh qua mo hinh DenseNet121 load tu file best_densenet.pth de du doan 1 trong 7 lop benh ly cua tap du lieu HAM10000. |
| **Giai doan 1: Core Pipeline & Ket noi** | Giai thich quyet dinh bang Grad-CAM | Tao lop GradCAMEngine trong gradcam_engine.py de trich xuat ban do kich hoat tai lop tich chap cuoi cung (features.norm5 cua DenseNet121). De tranh loi xung dot voi cac phep tinh ReLU bien doi tai cho, chuyen sang dang ky Tensor-level hook truc tiep tren tensor dau ra cua lop, dong thoi goi .clone() de nhan ban cac tensor activations va gradients. Dung .detach() ngat do thi dao ham truoc khi chuyen sang dinh dang NumPy array. |
| **Giai doan 1: Core Pipeline & Ket noi** | Xay dung API va giai quyet CORS | Viet endpoint chinh /api/analyze trong main.py nhan anh tai len duoi dang Multipart file, goi tuan tu YOLOv8 va DenseNet121 de xu ly, ve khung nhan va tron ban do nhiet bang OpenCV Colormap JET, sau do ma hoa Base64 tra ve client. Cau hinh allow_origins=["*"] tren CORSMiddleware cua FastAPI de cho phe client tu cong 3000 goi truc tiep sang cong 8000. |
| **Giai doan 2: Toi uu UI/UX & Tham so** | Tai thiet ke bo cuc hien thi | Thay doi bo cuc cu bang cach tach khung "Ket qua chan doan chi tiet" thanh mot hang rieng biet nam ngang o ben duoi. Hang phia tren hien thi song song anh goc cua nguoi dung tai len va anh chan doan (Grad-CAM overlay) de phuc vu doi chieu truc quan. |
| **Giai doan 2: Toi uu UI/UX & Tham so** | Trinh bay ket qua dang luoi | Hien thi thong tin chan doan chi tiet duoi dang cac the (cards) xep trong luoi CSS Grid. Thiet lap chieu rong toi thieu cho moi the la 280px (minmax(280px, 1fr)) de tu dong co gian deu dan tren ca tab Soi da va xem chi tiet Lich su benh an. Them thuoc tinh CSS whiteSpace: 'nowrap' cho tieu de vung va ten nhan y khoa de ngan chan hien tuong be dong van ban. |
| **Giai doan 2: Toi uu UI/UX & Tham so** | Tinh gian luong hoat dong | Loai bo thanh truot dieu chinh do mo (opacity slider) tai giao dien frontend va API tron anh /api/blend. Giao dien su dung anh ket qua da duoc tron san o backend voi ty le alpha = 0.5 de giam so luong request lien tuc va tang toc do hien thi giao dien. |
| **Giai doan 2: Toi uu UI/UX & Tham so** | Quan ly tham so mo hinh tap trung | Dua tham so YOLO_CONF_THRESHOLD = 0.25 va YOLO_BBOX_PADDING = 0.0 vao file cau hinh backend/app/config.py de de dang tinh chinh hieu nang phat hien ma khong can sua doi ma nguon xu ly anh. |
| **Giai doan 3: Phan tach Da ton thuong & Toi uu hoa** | Giai thuat tu dong tach Bounding Box | Thiet lap giai thuat hau xu ly lai ket hop YOLOv8 va Phan doan Cuong do anh xam (Intensity Segmentation) ket hop Phep dong Hinh thai hoc (Morphological Closing 5x5). Giai thuat tu dong phat hien khi nhieu not bi gop chung vao 1 BBox va tach thanh cac BBox con rieng biet chinh xac bao quanh tung ton thuong. |
| **Giai doan 3: Phan tach Da ton thuong & Toi uu hoa** | Tu dong lam khit Bounding Box long | Khi BBox phat hien cua YOLOv8 long leo hoac cat lech ton thuong, thuat toan su dung duong bao phan doan de tu dong dieu chinh toa do Bounding Box om khit hoan toan not ton thuong. |
| **Giai doan 3: Phan tach Da ton thuong & Toi uu hoa** | Nang cao tuong phan Grad-CAM | Tich hop hieu chinh Gamma (Gamma Correction voi gamma = 2.0) vao engine sinh ban do nhiet. Phep luy thua hoa giup tap trung cuong do mau do nong cuc dai vao nhan dam mau nguy hi cua ton thuong, dong thoi triet tieu nhieu kich hoat mo o vung da lanh xung quanh. |
| **Giai doan 3: Phan tach Da ton thuong & Toi uu hoa** | Nang cap mo hinh phat hien va phan loai | Nang cap len bo trong so V2 duoc huan luyen lai tren tap du lieu day du tu Kaggle: thay the mo hinh YOLOv8n mac dinh bang YOLOv8x lon va tinh chinh DenseNet121, cai thien dang ke do chinh xac dinh vi va phan loai. |

---

## Ket qua Thuc te & Giai thuat Tach Bounding Box (Multi-Lesion Splitting and Refinement)

### 1. Thach thuc lam sang
Mo hinh YOLOv8 duoc huan luyen tren bo du lieu da lieu HAM10000 (von chua hau het cac buc anh macro chup can canh mot ton thuong duy nhat). Khi ap dung vao thuc te voi anh chup lam sang goc rong chua nhieu ton thuong rai rac gan nhau, YOLOv8 co xu huong nhom toan bo cac not da nay vao **mot Bounding Box duy nhat**. Dieu nay dan den chan doan sai lech hoac bo sot cac not benh ly nguy hiem.

### 2. Giai phap ky thuat: Thuat toan Hậu xu ly lai (Hybrid Post-processing)
De giai quyet triet de van de nay ma khong can ton chi phi gan nhan lai du lieu, he thong tich hop giai thuat hau xu ly lai ket hop giua Hoc may (YOLOv8) va Thi giac may tinh truyen thong (Computer Vision) ngay tai Backend:

1. **Phat hien vung nghi ngo (YOLOv8)**: YOLOv8 quet va dua ra BBox bao quat vung da chua cac not ton thuong.
2. **Cat anh & Chuyen doi xam**: Vung anh ben trong BBox duoc cat ra (crop) va chuyen sang khong gian mau Grayscale.
3. **Phan doan dua tren do sang (Intensity Segmentation)**: Lam min bang Gaussian Blur (5x5) de loc bot nhieu va long to, sau do ap dung nguong nhi phan nghich dao (Inverse Thresholding voi nguong dong 125 cau hinh tai config.py) tan dung dac diem cac not ton thuong luon toi mau hon da lanh xung quanh.
4. **Phep dong hinh thai hoc (Morphological Closing)**: Ap dung phep dong voi hat nhan hinh elip kich thuoc 5x5 de lap day cac phan sang mau trang ben trong not (vi du: phan quang anh den chup) va ket noi cac mang dut gay cua cung mot not.
5. **Tim duong bao & Phan tach BBox**: Tim cac contours doc lap. Neu phat hien so luong duong bao hop le (dien tich >= 300 pixel) tu 2 tro len, he thong se tu dong huy bo BBox gop ban dau va sinh ra cac BBox con tuong ung om khit tung not. Cac not nay sau do duoc gui doc lap sang Stage 2 (DenseNet121) de phan loai va chay Grad-CAM rieng biet.

---

### 3. Ket qua thu nghiem lam sang thuc te

#### Truong hop 1: Chan doan nhieu ton thuong dong thoi (Multi-Lesion Detection)
Hinh anh thuc te khi chup vung da chua 3 not ton thuong hac to sap xep nam ngang. BBox lon ban dau cua YOLO da duoc tach chinh xac thanh 3 BBox con om khit, chan doan rieng biet ca 3 not deu la **Ung thu hac to Melanoma (MEL)** voi do tin cay cuc cao (>95%) kem ban do nhiet tap trung chuan xac:

![Chan doan nhieu ton thuong dong thoi](docs/assets/demo_multi_lesions.png)

#### Truong hop 2: Chan doan ton thuong lon kem cac not ruoi ve tinh nho
He thong phat hien chuan xac ton thuong chinh la **Ung thu hac to Melanoma (MEL)** dong thoi gom cum va dinh vi cac not ruoi ve tinh nho xung quanh la **Not ruoi hac to lanh tinh (NV)** ma khong bi bo sot hoac gop chung:

![Chan doan ton thuong lon kem cac not ruoi ve tinh nho](docs/assets/demo_single_lesion.png)

---

## Quy chuan Mau sac Nhan benh ly (Clinical Color Schema)

He thong su dung cac mau sac khac nhau de bieu thi muc do nghiem trong cua ton thuong tren vien Bounding Box va Badge nhan:

| Nhom benh ly | Nhan hien thi | Muc do benh ly | Mau sac hien thi |
| :--- | :--- | :--- | :--- |
| **mel** | Ung thu hac to Melanoma (MEL) | Ac tinh | Do sam / Danger |
| **bcc** | Ung thu bieu mo te bao day (BCC) | Ac tinh | Do tuoi / Danger |
| **akiec** | Day sung quang hoa (AKIEC) | Tien ung thu | Cam / Warning |
| **nv** | Not ruoi hac to (NV) | Lanh tinh | Xanh la / Success |
| **bkl** | Day sung lanh tinh (BKL) | Lanh tinh | Xanh la / Success |
| **df** | U soi da (DF) | Lanh tinh | Xanh la / Success |
| **vasc** | Ton thuong mach mau (VASC) | Lanh tinh | Xanh la / Success |

---

## Tai lieu Endpoints API

### 1. Phan tich hinh anh: POST /api/analyze
*   **Tham so (Form Data)**:
    *   file: File anh da can quet.
    *   alpha: He so do mo tron mau heatmap o backend (Mac dinh: 0.5).
*   **Phan hoi (JSON)**:
    ```json
    {
      "original_b64": "...", // Chuoi base64 anh goc
      "annotated_b64": "...", // Chuoi base64 anh da duoc ve khung va tron heatmap
      "lesions": [
        {
          "bbox": [173, 97, 517, 291], // Toa do [x1, y1, x2, y2]
          "label": "Not ruoi hac to (NV)", // Nhan tieng Viet
          "confidence": 0.8855, // Do tin cay (0.0 -> 1.0)
          "heatmap_b64": "..." // Anh heatmap tho cua rieng vung nay
        }
      ]
    }
    ```

### 2. Tron mau: POST /api/blend
*   **Tham so (JSON Body)**:
    *   original_b64: Anh goc dang base64.
    *   bboxes: Mang toa do cac bounding boxes.
    *   heatmaps_b64: Mang cac anh heatmap tho dang base64.
    *   labels: Danh sach chuoi nhan benh kem ty le tin cay.
    *   alpha: Do mo moi (0.0 -> 1.0).
*   **Phan hoi (JSON)**:
    ```json
    {
      "blended_b64": "..." // Chuoi base64 anh ket qua da tron mau moi
    }
    ```

---

## Cau truc thu muc

```
dermascan-ai/
├── docs/                            # Tai lieu du an va hinh anh minh hoa
│   └── assets/                      # Anh ket qua chan doan lam sang thuc te
├── backend/                         # Backend Python (FastAPI + AI Models)
│   ├── app/                         # Ma nguon ung dung chinh
│   │   ├── services/                # Cac dich vu phan tich AI doc lap
│   │   │   ├── densenet_classifier.py # Phan loai va tien xu ly (DenseNet121)
│   │   │   ├── gradcam_engine.py    # Engine trich xuat Grad-CAM qua Tensor Hook
│   │   │   ├── yolo_detector.py     # Phat hien vung nghi ton thuong (YOLOv8)
│   │   │   └── __init__.py
│   │   ├── utils/
│   │   │   ├── image_helper.py      # Xu ly cat anh, ve BBox va tron ban do mau JET
│   │   │   └── __init__.py
│   │   ├── config.py                # Cau hinh nguong loc tin cay YOLO, nhan HAM10000
│   │   ├── main.py                  # API endpoints, cau hinh Middleware CORS
│   │   └── __init__.py
│   ├── weights/                     # Chua cac file trong so cua mo hinh AI
│   │   ├── yolo_best.pt             # Trong so mo hinh YOLOv8
│   │   ├── best_densenet.pth        # Trong so mo hinh DenseNet121
│   │   └── classes.json             # File anh xa nhan
│   ├── run.py                       # Diem khoi chay ASGI server FastAPI
│   └── test_pipeline.py             # Script kiem tra pipeline chan doan ngoai tuyen
│
├── frontend/                        # Frontend Dashboard (Next.js + TypeScript)
│   ├── src/                         # Thu muc chua ma nguon ung dung
│   │   ├── app/                     # Next.js App Router, layout va styles
│   │   │   ├── globals.css          # Dinh nghia bien CSS va styles toan cuc
│   │   │   ├── layout.tsx           # Layout nen tang dung
│   │   │   └── page.tsx             # Trang Dashboard chinh
│   │   └── components/              # Cac UI Components lap ghep
│   │       ├── Header.tsx           # Tieu de ung dung
│   │       ├── ImageUploader.tsx    # Noi keo tha tai anh len
│   │       ├── ResultPanel.tsx      # Khung hien thi anh ket qua
│   │       └── Sidebar.tsx          # Thanh menu dieu huong ben trai
│   ├── next.config.js               # File cau hinh Next.js
│   ├── package.json                 # Quan ly dependencies va scripts chay ung dung
│   └── tsconfig.json                # Cau hinh trinh bien dich TypeScript
│
├── notebooks/                       # Thu muc luu tru tai lieu nghien cuu thu nghiem
│   └── test_pipeline.ipynb          # Jupyter Notebook chay thu nghiem pipeline
│
├── .gitignore                       # Danh sách các tệp loại trừ không đưa lên Git
└── requirements.txt                 # Quan ly thu vien Python chung cho toan du an
```
