'use client';

import { useEffect } from 'react';
import styles from './page.module.css';

export default function Home() {
  useEffect(() => {
    // Redirect to the static landing page
    window.location.href = '/index.html';
  }, []);

  return (
    <div className={styles.container}>
      <div className={styles.loading}>
        <p>Loading...</p>
      </div>
    </div>
  );
}