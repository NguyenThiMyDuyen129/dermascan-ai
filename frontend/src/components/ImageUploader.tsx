import React, { useRef, useState } from 'react';
import { UploadCloud } from 'lucide-react';

interface ImageUploaderProps {
  onImageSelected: (file: File) => void;
  selectedImage: string | null;
}

export default function ImageUploader({ onImageSelected, selectedImage }: ImageUploaderProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onImageSelected(e.target.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onImageSelected(e.dataTransfer.files[0]);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  return (
    <div
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      onClick={triggerFileInput}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        ...styles.uploaderBox,
        borderColor: isDragOver ? 'var(--color-accent)' : 'var(--color-text-primary)',
        backgroundColor: isDragOver ? '#FFF8F6' : '#F8FAFC',
      }}
    >
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        accept="image/*"
        style={{ display: 'none' }}
      />
      {selectedImage ? (
        <div style={styles.previewContainer}>
          <img src={selectedImage} alt="Preview" style={styles.previewImage} />
          <div 
            style={{
              ...styles.changeOverlay,
              opacity: isHovered ? 1 : 0
            }}
          >
            <UploadCloud size={20} color="#FFFFFF" />
            <span style={styles.changeText}>Thay đổi ảnh</span>
          </div>
        </div>
      ) : (
        <div style={styles.placeholderContainer}>
          <UploadCloud size={44} color="var(--color-text-primary)" style={styles.icon} />
          <p style={styles.primaryText}>Kéo thả hoặc nhấn để tải ảnh tổn thương da</p>
          <p style={styles.secondaryText}>Chấp nhận file ảnh (PNG, JPG, JPEG)</p>
        </div>
      )}
    </div>
  );
}

const styles = {
  uploaderBox: {
    height: '400px',
    border: '2px dashed var(--color-text-primary)',
    borderRadius: '12px',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    cursor: 'pointer',
    transition: 'all 0.2s ease',
    overflow: 'hidden',
    position: 'relative' as const,
  },
  placeholderContainer: {
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    textAlign: 'center' as const,
    padding: '20px',
  },
  icon: {
    marginBottom: '15px',
  },
  primaryText: {
    fontWeight: 700,
    fontSize: '1.05rem',
    marginBottom: '8px',
  },
  secondaryText: {
    fontSize: '0.85rem',
    color: 'var(--color-text-secondary)',
  },
  previewContainer: {
    width: '100%',
    height: '100%',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  previewImage: {
    width: '100%',
    height: '100%',
    objectFit: 'contain' as const,
  },
  changeOverlay: {
    position: 'absolute' as const,
    bottom: 0,
    left: 0,
    right: 0,
    height: '50px',
    backgroundColor: 'rgba(10, 37, 64, 0.8)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    gap: '8px',
    color: '#FFFFFF',
    fontWeight: 600,
    fontSize: '0.9rem',
    transition: 'opacity 0.2s ease',
  },
  changeText: {
    fontFamily: 'var(--font-body)',
  }
};
