import torch
import torch.nn as nn
import numpy as np
import cv2

class GradCAMEngine:
    def __init__(self, model: nn.Module, target_layer: nn.Module):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        self.handlers = []
        
        # Đăng ký hooks để lấy activations và gradients của layer mục tiêu
        self.handlers.append(self.target_layer.register_forward_hook(self.forward_hook))
        if hasattr(self.target_layer, 'register_full_backward_hook'):
            self.handlers.append(self.target_layer.register_full_backward_hook(self.backward_hook))
        else:
            self.handlers.append(self.target_layer.register_backward_hook(self.backward_hook))

    def forward_hook(self, module, input, output):
        self.activations = output.detach()

    def backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()

    def remove_hooks(self):
        for handler in self.handlers:
            handler.remove()

    def generate_heatmap(self, input_tensor: torch.Tensor, target_class_idx: int):
        """
        Sinh heatmap Grad-CAM cho class mục tiêu
        """
        self.model.zero_grad()
        output = self.model(input_tensor)
        
        # Chọn class target để tính đạo hàm ngược
        score = output[0][target_class_idx]
        score.backward(retain_graph=True)
        
        # Tính toán Grad-CAM
        gradients = self.gradients[0]      # Shape: (C, H, W)
        activations = self.activations[0]  # Shape: (C, H, W)
        
        # Global Average Pooling cho gradients
        weights = torch.mean(gradients, dim=(1, 2))  # Shape: (C,)
        
        # Nhân tuyến tính các activations và weights
        grad_cam = torch.zeros(activations.shape[1:], dtype=torch.float32, device=activations.device)
        for i, w in enumerate(weights):
            grad_cam += w * activations[i]
            
        # Áp dụng ReLU (chỉ giữ lại các đặc trưng kích hoạt tích cực)
        grad_cam = torch.clamp(grad_cam, min=0)
        
        # Chuẩn hóa về [0, 1]
        if grad_cam.max() > 0:
            grad_cam = grad_cam / grad_cam.max()
            
        heatmap = grad_cam.cpu().numpy()
        return heatmap
