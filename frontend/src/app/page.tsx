'use client';

import React, { useState } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import ImageUploader from '../components/ImageUploader';
import ResultPanel from '../components/ResultPanel';
import { Activity, History, AlertCircle, Info } from 'lucide-react';

interface Lesion {
  bbox: number[];
  label: string;
  confidence: number;
  heatmap_b64: string;
}

interface AnalysisResult {
  original_b64: string;
  annotated_b64: string;
  lesions: Lesion[];
  timestamp: string;
  fileName: string;
}

export default function Home() {
  const [activeTab, setActiveTab] = useState('scan');
  
  // Trạng thái quét của tab Scan
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  
  // Lịch sử chẩn đoán
  const [historyList, setHistoryList] = useState<AnalysisResult[]>([]);
  const [selectedHistory, setSelectedHistory] = useState<AnalysisResult | null>(null);

  const handleImageSelected = (file: File) => {
    setSelectedFile(file);
    setErrorMsg(null);
    setResult(null);
    
    // Đọc file để tạo preview url
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreviewUrl(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) {
      setErrorMsg("Vui lòng tải ảnh lên trước khi phân tích!");
      return;
    }
    
    setIsAnalyzing(true);
    setErrorMsg(null);
    
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
      const response = await fetch('/api/analyze?alpha=0.5', {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error("Không thể kết nối với server phân tích.");
      }
      
      const data = await response.json();
      
      const newResult: AnalysisResult = {
        original_b64: data.original_b64,
        annotated_b64: data.annotated_b64,
        lesions: data.lesions,
        timestamp: new Date().toLocaleString('vi-VN'),
        fileName: selectedFile.name
      };
      
      setResult(newResult);
      setHistoryList(prev => [newResult, ...prev]);
    } catch (e: any) {
      setErrorMsg(e.message || "Đã xảy ra lỗi trong quá trình phân tích ảnh.");
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar bên trái */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <div className="main-content">
        {/* Header ở trên */}
        <Header />
        
        {/* Nội dung thay đổi theo Tab */}
        <main className="page-body">
          {activeTab === 'scan' ? (
            <div>
              {/* Tiêu đề trang */}
              <div style={styles.titleSection}>
                <h2 style={styles.pageTitle}>Phân tích & Phát hiện Tổn thương Da</h2>
                <p style={styles.pageSubtitle}>
                  Tải ảnh chụp vùng da lên. Hệ thống sẽ phát hiện vị trí tổn thương (YOLOv8) và chẩn đoán bệnh lý kèm bản đồ nhiệt giải thích (DenseNet + Grad-CAM).
                </p>
              </div>

              {errorMsg && (
                <div style={styles.errorBanner}>
                  <AlertCircle size={20} color="var(--color-danger)" />
                  <span style={styles.errorText}>{errorMsg}</span>
                </div>
              )}

              {/* Bố cục song song hai cột */}
              <div style={styles.grid}>
                {/* Cột trái: Tải ảnh & Hành động */}
                <div className="card-panel" style={styles.column}>
                  <h3 style={styles.panelTitle}>1. Ảnh đầu vào</h3>
                  <div style={styles.uploaderWrapper}>
                    <ImageUploader 
                      onImageSelected={handleImageSelected} 
                      selectedImage={previewUrl} 
                    />
                  </div>
                  
                  <button 
                    onClick={handleAnalyze} 
                    disabled={isAnalyzing || !selectedFile}
                    style={{
                      ...styles.analyzeBtn,
                      opacity: (isAnalyzing || !selectedFile) ? 0.6 : 1,
                      cursor: (isAnalyzing || !selectedFile) ? 'not-allowed' : 'pointer'
                    }}
                  >
                    {isAnalyzing ? (
                      <div style={styles.loaderContainer}>
                        <div style={styles.spinner}></div>
                        <span>Đang xử lý phân tích...</span>
                      </div>
                    ) : (
                      "🚀 BẮT ĐẦU PHÂN TÍCH Y KHOA"
                    )}
                  </button>
                </div>

                {/* Cột phải: Bản đồ chẩn đoán & Kết quả */}
                <div className="card-panel" style={styles.column}>
                  <h3 style={styles.panelTitle}>2. Bản đồ chẩn đoán</h3>
                  {result ? (
                    <ResultPanel 
                      originalB64={result.original_b64}
                      annotatedB64={result.annotated_b64}
                      lesions={result.lesions}
                    />
                  ) : (
                    <div style={styles.emptyState}>
                      <Activity size={48} color="var(--color-text-secondary)" style={styles.emptyIcon} />
                      <p style={styles.emptyText}>Bản đồ nhiệt và kết quả sẽ hiển thị sau khi hoàn tất phân tích ảnh ở cột bên trái.</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ) : (
            /* Tab Lịch sử */
            <div className="card-panel" style={{ minHeight: '500px' }}>
              <div style={styles.titleSection}>
                <h2 style={styles.pageTitle}>Lịch sử chẩn đoán bệnh án</h2>
                <p style={styles.pageSubtitle}>Xem lại các lượt quét tổn thương da đã thực hiện trong phiên làm việc hiện tại.</p>
              </div>

              {historyList.length === 0 ? (
                <div style={styles.emptyState}>
                  <History size={48} color="var(--color-text-secondary)" style={styles.emptyIcon} />
                  <p style={styles.emptyText}>Chưa có lịch sử quét nào được ghi nhận.</p>
                </div>
              ) : (
                <div style={styles.historyLayout}>
                  {/* Danh sách bên trái */}
                  <div style={styles.historyListColumn}>
                    {historyList.map((item, idx) => (
                      <button 
                        key={idx} 
                        onClick={() => setSelectedHistory(item)}
                        style={{
                          ...styles.historyItemBtn,
                          borderColor: selectedHistory === item ? 'var(--color-accent)' : 'var(--color-border)',
                          backgroundColor: selectedHistory === item ? '#FFF8F6' : '#FFFFFF'
                        }}
                      >
                        <div style={styles.historyItemMeta}>
                          <span style={styles.historyTime}>{item.timestamp}</span>
                          <span style={styles.historyFileName}>{item.fileName}</span>
                        </div>
                        <span style={styles.historyCountBadge}>
                          {item.lesions.length} tổn thương
                        </span>
                      </button>
                    ))}
                  </div>

                  {/* Chi tiết bên phải */}
                  <div style={styles.historyDetailColumn}>
                    {selectedHistory ? (
                      <ResultPanel 
                        originalB64={selectedHistory.original_b64}
                        annotatedB64={selectedHistory.annotated_b64}
                        lesions={selectedHistory.lesions}
                      />
                    ) : (
                      <div style={styles.emptyDetailState}>
                        <Info size={32} color="var(--color-text-secondary)" />
                        <p style={styles.emptyText}>Chọn một bệnh án trong danh sách lịch sử để xem chi tiết bản đồ chẩn đoán.</p>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </main>
      </div>

      {/* Style phụ hỗ trợ animation spin */}
      <style jsx global>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

const styles = {
  titleSection: {
    marginBottom: '25px',
  },
  pageTitle: {
    fontSize: '1.8rem',
    fontWeight: 800,
    color: 'var(--color-text-primary)',
    marginBottom: '6px',
    letterSpacing: '-0.5px',
  },
  pageSubtitle: {
    color: 'var(--color-text-secondary)',
    fontSize: '0.95rem',
    lineHeight: 1.5,
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '30px',
  },
  column: {
    display: 'flex',
    flexDirection: 'column' as const,
    minHeight: '600px',
  },
  panelTitle: {
    fontSize: '1.15rem',
    fontWeight: 700,
    marginBottom: '15px',
    borderBottom: '2px solid var(--color-border)',
    paddingBottom: '10px',
    color: 'var(--color-text-primary)',
  },
  uploaderWrapper: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column' as const,
    justifyContent: 'center',
    marginBottom: '20px',
  },
  analyzeBtn: {
    width: '100%',
    padding: '16px',
    backgroundColor: 'var(--color-accent)',
    color: '#FFFFFF',
    border: 'none',
    borderRadius: '8px',
    fontWeight: 700,
    fontSize: '1.05rem',
    boxShadow: '0 4px 12px rgba(255, 107, 53, 0.3)',
    transition: 'all 0.2s ease',
  },
  loaderContainer: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
  },
  spinner: {
    width: '20px',
    height: '20px',
    border: '3px solid rgba(255, 255, 255, 0.3)',
    borderTop: '3px solid #FFFFFF',
    borderRadius: '50%',
    animation: 'spin 0.8s linear infinite',
  },
  errorBanner: {
    backgroundColor: 'rgba(239, 68, 68, 0.08)',
    border: '1px solid var(--color-danger)',
    borderRadius: '8px',
    padding: '12px 15px',
    marginBottom: '25px',
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  errorText: {
    color: 'var(--color-danger)',
    fontWeight: 600,
    fontSize: '0.9rem',
  },
  emptyState: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    justifyContent: 'center',
    padding: '40px',
    textAlign: 'center' as const,
    border: '2px dashed var(--color-border)',
    borderRadius: '12px',
    backgroundColor: '#F8FAFC',
  },
  emptyIcon: {
    marginBottom: '15px',
  },
  emptyText: {
    color: 'var(--color-text-secondary)',
    fontSize: '0.9rem',
    lineHeight: 1.5,
    maxWidth: '300px',
  },
  // Lịch sử
  historyLayout: {
    display: 'grid',
    gridTemplateColumns: '320px 1fr',
    gap: '30px',
    marginTop: '20px',
  },
  historyListColumn: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '12px',
    maxHeight: '600px',
    overflowY: 'auto' as const,
  },
  historyItemBtn: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px',
    borderRadius: '8px',
    border: '1px solid',
    textAlign: 'left' as const,
    cursor: 'pointer',
    transition: 'all 0.2s ease',
  },
  historyItemMeta: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '4px',
  },
  historyTime: {
    fontSize: '0.75rem',
    color: 'var(--color-text-secondary)',
    fontWeight: 500,
  },
  historyFileName: {
    fontSize: '0.9rem',
    fontWeight: 700,
    color: 'var(--color-text-primary)',
    maxWidth: '180px',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap' as const,
  },
  historyCountBadge: {
    fontSize: '0.75rem',
    backgroundColor: '#F1F5F9',
    padding: '4px 8px',
    borderRadius: '12px',
    fontWeight: 600,
    color: 'var(--color-text-primary)',
  },
  historyDetailColumn: {
    border: '1px solid var(--color-border)',
    borderRadius: '12px',
    padding: '24px',
    backgroundColor: '#FFFFFF',
    minHeight: '500px',
  },
  emptyDetailState: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column' as const,
    alignItems: 'center',
    justifyContent: 'center',
    gap: '10px',
    color: 'var(--color-text-secondary)',
    textAlign: 'center' as const,
  }
};
