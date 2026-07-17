import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import cv2
import os
from ..config import DENSENET_MODEL_NAME, CLASS_NAMES, DENSENET_WEIGHTS_PATH

class DenseNetClassifier:
    def __init__(self, pretrained: bool = True):
        # Khởi tạo thiết bị chạy (CPU hoặc GPU)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Load DenseNet121 từ torchvision
        if DENSENET_MODEL_NAME == "densenet121":
            if pretrained:
                from torchvision.models import DenseNet121_Weights
                self.model = models.densenet121(weights=DenseNet121_Weights.DEFAULT)
            else:
                self.model = models.densenet121(weights=None)
            # Thay đổi lớp classifier cuối cùng phù hợp với số nhãn (Benign, Malignant, Inflammatory)
            num_ftrs = self.model.classifier.in_features
            self.model.classifier = torch.nn.Linear(num_ftrs, len(CLASS_NAMES))
            
            # Nạp custom weights nếu có
            if os.path.exists(DENSENET_WEIGHTS_PATH):
                try:
                    self.model.load_state_dict(torch.load(DENSENET_WEIGHTS_PATH, map_location=self.device))
                    print(f"[INFO] Loaded custom DenseNet weights from {DENSENET_WEIGHTS_PATH}")
                except Exception as e:
                    print(f"[WARNING] Failed to load custom weights from {DENSENET_WEIGHTS_PATH}: {e}. Using pre-trained ImageNet weights.")
            
        self.model.to(self.device)
        self.model.eval()

        # Định nghĩa tiền xử lý ảnh cho DenseNet
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def preprocess(self, crop_img: np.ndarray):
        """Chuyển đổi numpy array (BGR từ OpenCV) sang PyTorch Tensor đã chuẩn hóa"""
        rgb_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)
        tensor_img = self.transform(pil_img).unsqueeze(0)  # (1, 3, 224, 224)
        return tensor_img.to(self.device)

    def classify(self, crop_img: np.ndarray):
        """Phân loại ảnh đã cắt và trả về lớp dự đoán kèm xác suất"""
        input_tensor = self.preprocess(crop_img)
        with torch.no_grad():
            outputs = self.model(input_tensor)
            probabilities = torch.softmax(outputs, dim=1)[0].cpu().numpy().tolist()
            
        max_idx = np.argmax(probabilities)
        pred_label = CLASS_NAMES[max_idx]
        pred_conf = probabilities[max_idx]
        
        return pred_label, pred_conf, probabilities
