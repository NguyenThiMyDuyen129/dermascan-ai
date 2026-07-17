import React from 'react';
import { ShieldAlert, History } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export default function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
  const menuItems = [
    { id: 'scan', label: 'Bộ quét tổn thương', icon: ShieldAlert },
    { id: 'history', label: 'Lịch sử chẩn đoán', icon: History },
  ];

  return (
    <aside style={styles.sidebar}>
      <nav style={styles.nav}>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              style={{
                ...styles.menuButton,
                backgroundColor: isActive ? 'var(--color-accent)' : 'transparent',
                color: isActive ? '#FFFFFF' : '#B8C2CC',
              }}
            >
              <Icon size={20} />
              <span style={styles.labelText}>{item.label}</span>
            </button>
          );
        })}
      </nav>
      <div style={styles.footer}>
        <p style={styles.version}>DermaScan AI v1.0</p>
      </div>
    </aside>
  );
}

const styles = {
  sidebar: {
    width: '260px',
    backgroundColor: 'var(--color-text-primary)', /* Xanh đậm */
    display: 'flex',
    flexDirection: 'column' as const,
    justifyContent: 'space-between',
    padding: '30px 20px',
  },
  nav: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '12px',
  },
  menuButton: {
    display: 'flex',
    alignItems: 'center',
    gap: '15px',
    padding: '14px 18px',
    borderRadius: '8px',
    border: 'none',
    cursor: 'pointer',
    fontSize: '0.95rem',
    fontWeight: 600,
    transition: 'all 0.2s ease',
    textAlign: 'left' as const,
    width: '100%',
  },
  labelText: {
    fontFamily: 'var(--font-system)',
  },
  footer: {
    textAlign: 'center' as const,
    borderTop: '1px solid #1A365D',
    paddingTop: '20px',
  },
  version: {
    color: '#627D98',
    fontSize: '0.8rem',
  }
};
