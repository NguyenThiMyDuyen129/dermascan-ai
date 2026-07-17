import React from 'react';
import { Stethoscope } from 'lucide-react';

export default function Header() {
  return (
    <header style={styles.header}>
      <div style={styles.brand}>
        <Stethoscope size={28} color="var(--color-accent)" />
        <span style={styles.title}>DermaScan AI</span>
      </div>
      <div style={styles.info}>
        <span style={styles.badge}>Medical Assistant Mode</span>
      </div>
    </header>
  );
}

const styles = {
  header: {
    height: '70px',
    backgroundColor: '#FFFFFF',
    borderBottom: '2px solid var(--color-text-primary)',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '0 30px',
    boxShadow: '0 2px 10px rgba(10, 37, 64, 0.03)',
  },
  brand: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  title: {
    fontFamily: 'var(--font-system)',
    fontSize: '1.4rem',
    fontWeight: 800,
    color: 'var(--color-text-primary)',
    letterSpacing: '-0.5px',
  },
  info: {
    display: 'flex',
    alignItems: 'center',
  },
  badge: {
    fontSize: '0.85rem',
    fontWeight: 700,
    backgroundColor: 'rgba(255, 107, 53, 0.1)',
    color: 'var(--color-accent)',
    padding: '6px 12px',
    borderRadius: '20px',
    border: '1px solid var(--color-accent)',
  }
};
