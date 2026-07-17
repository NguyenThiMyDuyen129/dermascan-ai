import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'DermaScan AI - Skin Lesion Localization & Explainability',
  description: 'Hệ thống Phân tích, Khoanh vùng & Giải thích Tổn thương Da sử dụng YOLOv8 và DenseNet',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi">
      <body>{children}</body>
    </html>
  );
}
