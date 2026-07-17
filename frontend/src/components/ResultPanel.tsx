import React from 'react';

interface Lesion {
  bbox: number[];
  label: string;
  confidence: number;
  heatmap_b64: string;
}

interface ResultPanelProps {
  originalB64: string;
  annotatedB64: string;
  lesions: Lesion[];
}

export default function ResultPanel({ originalB64, annotatedB64, lesions }: ResultPanelProps) {
  return (
    <div style={styles.container}>
      {/* Khung ảnh */}
      <div style={styles.imageFrame}>
        <img 
          src={`data:image/jpeg;base64,${annotatedB64}`} 
          alt="Bản đồ chẩn đoán" 
          style={styles.resultImage} 
        />
      </div>

      {/* Chú thích màu sắc */}
      <div style={styles.legend}>
        <div style={styles.legendItem}>
          <span style={{ ...styles.legendDot, backgroundColor: 'var(--color-success)' }}></span>
          <span style={styles.legendText}>Lành tính (NV, BKL, DF, VASC)</span>
        </div>
        <div style={styles.legendItem}>
          <span style={{ ...styles.legendDot, backgroundColor: 'var(--color-danger)' }}></span>
          <span style={styles.legendText}>Ác tính (MEL, BCC)</span>
        </div>
        <div style={styles.legendItem}>
          <span style={{ ...styles.legendDot, backgroundColor: 'var(--color-warning)' }}></span>
          <span style={styles.legendText}>Tiền ung thư (AKIEC)</span>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '20px',
    height: '100%',
  },
  imageFrame: {
    flex: 1,
    minHeight: '380px',
    border: '2px solid var(--color-text-primary)',
    borderRadius: '12px',
    backgroundColor: '#F8FAFC',
    overflow: 'hidden',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  resultImage: {
    width: '100%',
    height: '100%',
    objectFit: 'contain' as const,
  },
  legend: {
    display: 'flex',
    justifyContent: 'center',
    gap: '20px',
    padding: '10px 0',
    borderTop: '1px solid var(--color-border)',
  },
  legendItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px',
  },
  legendDot: {
    width: '10px',
    height: '10px',
    borderRadius: '50%',
    display: 'inline-block',
  },
  legendText: {
    fontSize: '0.8rem',
    fontWeight: 600,
    color: 'var(--color-text-secondary)',
  }
};
