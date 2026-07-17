import React, { useState, useEffect, useRef } from 'react';
import { Sliders, ClipboardList } from 'lucide-react';

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
  const [alpha, setAlpha] = useState(0.5);
  const [blendedB64, setBlendedB64] = useState(annotatedB64);
  const [isBlending, setIsBlending] = useState(false);
  const latestAlpha = useRef(0.5);

  // Cập nhật lại ảnh khi lesions thay đổi (lần quét mới)
  useEffect(() => {
    setBlendedB64(annotatedB64);
    setAlpha(0.5);
    latestAlpha.current = 0.5;
  }, [annotatedB64, lesions]);

  const performBlend = async (val: number) => {
    if (isBlending) return;
    setIsBlending(true);
    
    try {
      const response = await fetch('/api/blend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          original_b64: originalB64,
          bboxes: lesions.map(l => l.bbox),
          heatmaps_b64: lesions.map(l => l.heatmap_b64),
          labels: lesions.map(l => `${l.label} (${(l.confidence * 100).toFixed(2)}%)`),
          alpha: val
        })
      });
      const data = await response.json();
      if (data.blended_b64) {
        setBlendedB64(data.blended_b64);
      }
    } catch (e) {
      console.error("Lỗi khi trộn ảnh:", e);
    } finally {
      setIsBlending(false);
      // Nếu người dùng đã kéo tới vị trí khác trong lúc đang call API, gọi tiếp vị trí mới nhất
      if (latestAlpha.current !== val) {
        performBlend(latestAlpha.current);
      }
    }
  };

  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = parseFloat(e.target.value);
    setAlpha(val);
    latestAlpha.current = val;
    performBlend(val);
  };

  const getClassColor = (label: string) => {
    const l = label.toLowerCase();
    if (l.includes('malignant') || l.includes('ác tính')) return 'var(--color-danger)';
    if (l.includes('inflammatory') || l.includes('viêm')) return 'var(--color-warning)';
    return 'var(--color-success)'; // Benign
  };

  return (
    <div style={styles.container}>
      {/* Khung ảnh */}
      <div style={styles.imageFrame}>
        <img 
          src={`data:image/jpeg;base64,${blendedB64}`} 
          alt="Bản đồ chẩn đoán" 
          style={styles.resultImage} 
        />
      </div>

      {/* Điều khiển Opacity */}
      <div style={styles.controls}>
        <div style={styles.sliderLabel}>
          <div style={styles.iconText}>
            <Sliders size={18} color="var(--color-text-primary)" />
            <span style={styles.labelTitle}>Độ mờ Bản đồ nhiệt (Grad-CAM Opacity)</span>
          </div>
          <span style={styles.sliderVal}>{(alpha * 100).toFixed(0)}%</span>
        </div>
        <input 
          type="range" 
          min="0.0" 
          max="1.0" 
          step="0.05" 
          value={alpha} 
          onChange={handleSliderChange}
        />
      </div>

      {/* Danh sách tổn thương chi tiết */}
      <div style={styles.diagnosisSection}>
        <div style={styles.sectionHeader}>
          <ClipboardList size={20} color="var(--color-text-primary)" />
          <h3 style={styles.sectionTitle}>Kết quả chẩn đoán chi tiết</h3>
        </div>
        {lesions.length === 0 ? (
          <div style={styles.emptyDiagnosis}>Không phát hiện tổn thương nào trên da.</div>
        ) : (
          <div style={styles.lesionList}>
            {lesions.map((lesion, index) => (
              <div key={index} style={styles.lesionCard}>
                <div style={styles.lesionHeader}>
                  <span style={styles.lesionIndex}>Vùng {index + 1}</span>
                  <span 
                    style={{
                      ...styles.lesionBadge,
                      backgroundColor: getClassColor(lesion.label) + '15',
                      color: getClassColor(lesion.label),
                      borderColor: getClassColor(lesion.label)
                    }}
                  >
                    {lesion.label}
                  </span>
                </div>
                <div style={styles.lesionBody}>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Độ tin cậy:</span>
                    <span style={styles.infoValue}>{(lesion.confidence * 100).toFixed(2)}%</span>
                  </div>
                  <div style={styles.infoRow}>
                    <span style={styles.infoLabel}>Tọa độ (BBox):</span>
                    <span style={styles.infoValue}>[{lesion.bbox.join(', ')}]</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Chú thích màu sắc */}
      <div style={styles.legend}>
        <div style={styles.legendItem}>
          <span style={{ ...styles.legendDot, backgroundColor: 'var(--color-success)' }}></span>
          <span style={styles.legendText}>Lành tính (Benign)</span>
        </div>
        <div style={styles.legendItem}>
          <span style={{ ...styles.legendDot, backgroundColor: 'var(--color-danger)' }}></span>
          <span style={styles.legendText}>Ác tính (Malignant)</span>
        </div>
        <div style={styles.legendItem}>
          <span style={{ ...styles.legendDot, backgroundColor: 'var(--color-warning)' }}></span>
          <span style={styles.legendText}>Viêm nhiễm (Inflammatory)</span>
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
  },
  imageFrame: {
    height: '400px',
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
  controls: {
    backgroundColor: '#F8FAFC',
    border: '1px solid var(--color-border)',
    borderRadius: '8px',
    padding: '15px 20px',
  },
  sliderLabel: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
  },
  iconText: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
  },
  labelTitle: {
    fontWeight: 700,
    fontSize: '0.9rem',
    fontFamily: 'var(--font-system)',
  },
  sliderVal: {
    fontWeight: 800,
    color: 'var(--color-accent)',
    fontFamily: 'var(--font-system)',
  },
  diagnosisSection: {
    border: '2px solid var(--color-text-primary)',
    borderRadius: '12px',
    padding: '20px',
    backgroundColor: '#FFFFFF',
  },
  sectionHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    borderBottom: '1px solid var(--color-border)',
    paddingBottom: '12px',
    marginBottom: '15px',
  },
  sectionTitle: {
    fontSize: '1.05rem',
    fontWeight: 700,
    fontFamily: 'var(--font-system)',
  },
  emptyDiagnosis: {
    color: 'var(--color-text-secondary)',
    fontSize: '0.9rem',
    textAlign: 'center' as const,
    padding: '10px 0',
  },
  lesionList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '12px',
    maxHeight: '220px',
    overflowY: 'auto' as const,
    paddingRight: '5px',
  },
  lesionCard: {
    border: '1px solid var(--color-border)',
    borderRadius: '8px',
    padding: '12px 15px',
    backgroundColor: '#F8FAFC',
  },
  lesionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px',
  },
  lesionIndex: {
    fontWeight: 700,
    fontSize: '0.9rem',
  },
  lesionBadge: {
    fontSize: '0.8rem',
    fontWeight: 700,
    padding: '3px 8px',
    borderRadius: '12px',
    border: '1px solid',
  },
  lesionBody: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '5px',
  },
  infoRow: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '0.85rem',
  },
  infoLabel: {
    color: 'var(--color-text-secondary)',
  },
  infoValue: {
    fontWeight: 600,
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
