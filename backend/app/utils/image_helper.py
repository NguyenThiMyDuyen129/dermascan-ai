import cv2
import numpy as np

def crop_bounding_boxes(image: np.ndarray, bboxes: list, padding_ratio: float = 0.25):
    """
    Cắt các ảnh con (lesion crops) từ ảnh gốc dựa trên danh sách bounding boxes có bổ sung padding.
    bboxes: list of [x1, y1, x2, y2, conf, cls_id]
    Trả về: danh sách các ảnh con (np.ndarray) và tọa độ đã được chuẩn hóa (int).
    """
    h, w = image.shape[:2]
    crops = []
    refined_bboxes = []
    
    for box in bboxes:
        bx1, by1, bx2, by2 = box[0], box[1], box[2], box[3]
        bw = bx2 - bx1
        bh = by2 - by1
        
        # Thêm padding xung quanh bounding box
        pad_w = bw * padding_ratio
        pad_h = bh * padding_ratio
        
        x1 = max(0, int(round(bx1 - pad_w)))
        y1 = max(0, int(round(by1 - pad_h)))
        x2 = min(w, int(round(bx2 + pad_w)))
        y2 = min(h, int(round(by2 + pad_h)))
        
        # Đảm bảo box hợp lệ
        if (x2 - x1) > 0 and (y2 - y1) > 0:
            crop = image[y1:y2, x1:x2].copy()
            crops.append(crop)
            refined_bboxes.append([x1, y1, x2, y2, box[4], box[5]])
            
    return crops, refined_bboxes

def blend_all(image: np.ndarray, bboxes: list, heatmaps: list, labels: list, alpha: float):
    """
    Trộn toàn bộ heatmap vào ảnh gốc tại các bounding box tương ứng và vẽ khung nhãn.
    image: ảnh gốc (BGR)
    bboxes: list của refined bboxes [x1, y1, x2, y2, conf, cls_id]
    heatmaps: danh sách các heatmap thô (np.ndarray cùng kích thước crop hoặc 2D [0, 1])
    labels: danh sách các nhãn kèm độ tin cậy (ví dụ: ["Malignant (92%)", ...])
    alpha: độ mờ của heatmap (0.0 đến 1.0)
    """
    out_img = image.copy()
    
    # Định nghĩa 7 màu sắc đặc trưng BGR cho 7 nhóm tổn thương HAM10000
    colors = [
        (0, 140, 255),  # akiec (Dày sừng quang hóa) - Cam
        (0, 0, 255),    # bcc (Ung thư biểu mô TB đáy) - Đỏ tươi (Ác tính)
        (0, 255, 0),    # bkl (Dày sừng lành tính) - Xanh lá
        (100, 255, 100),# df (U sợi da) - Xanh lá nhạt
        (0, 0, 180),    # mel (Ung thư hắc tố Melanoma) - Đỏ sẫm (Ác tính nguy hiểm)
        (255, 200, 0),  # nv (Nốt ruồi hắc tố) - Xanh dương nhạt (Lành tính)
        (200, 0, 200)   # vasc (Tổn thương mạch máu) - Tím
    ]

    for box, heatmap, label in zip(bboxes, heatmaps, labels):
        x1, y1, x2, y2 = box[:4]
        cls_id = int(box[5])
        color = colors[cls_id % len(colors)]
        
        # 1. Trộn Heatmap nếu alpha > 0 và có heatmap
        if alpha > 0 and heatmap is not None:
            crop_w, crop_h = (x2 - x1), (y2 - y1)
            # Resize heatmap về kích thước của crop
            heatmap_resized = cv2.resize(heatmap, (crop_w, crop_h))
            # Chuyển heatmap sang dạng 0-255
            heatmap_uint8 = np.uint8(255 * heatmap_resized)
            # Áp dụng Colormap JET
            heatmap_color = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
            
            # Trộn với vùng ảnh crop gốc
            crop_orig = out_img[y1:y2, x1:x2]
            blended_crop = cv2.addWeighted(heatmap_color, alpha, crop_orig, 1.0 - alpha, 0)
            out_img[y1:y2, x1:x2] = blended_crop
            
        # 2. Vẽ Bounding Box & Label
        cv2.rectangle(out_img, (x1, y1), (x2, y2), color, 3)
        
        # Vẽ background cho text label
        text = f"{label}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2
        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        
        text_w, text_h = text_size
        cv2.rectangle(out_img, (x1, y1 - text_h - 10), (x1 + text_w, y1), color, -1)
        cv2.putText(out_img, text, (x1, y1 - 5), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
        
    return out_img
