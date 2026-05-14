'use client';

import { useState, useEffect } from 'react';
import styles from './page.module.css';

interface DesignSystem {
  id: string;
  name: string;
  category: string;
  description: string;
  preview: {
    bg: string;
    text: string;
    accent: string;
  };
}

interface GenerateResponse {
  id: string;
  status: string;
  preview_url?: string;
  html_base64?: string;
}

export default function Home() {
  const [step, setStep] = useState(1);
  const [designs, setDesigns] = useState<DesignSystem[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState('');

  // Form state
  const [formData, setFormData] = useState({
    name: '',
    role: '',
    bio: '',
    short_story: '',
    full_story: '',
    mbti: 'INFP',
    design: 'notion',
    email: '',
    wechat: '',
    link: '',
  });

  useEffect(() => {
    // Fetch designs on mount
    fetch('/api/designs')
      .then(res => res.json())
      .then(data => setDesigns(data.designs || []))
      .catch(console.error);
  }, []);

  const mbtiTypes = ['INFJ', 'INFP', 'ENFJ', 'ENFP', 'INTJ', 'ENTP', 'ESFP', 'ISFJ'];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          product: 'personal_site',
          design: formData.design,
          content: {
            name: formData.name,
            role: formData.role,
            bio: formData.bio,
            short_story: formData.short_story,
            full_story: formData.full_story,
            mbti: formData.mbti,
            highlights: [],
            contact: {
              email: formData.email,
              wechat: formData.wechat,
              link: formData.link,
            },
          },
          selected_modules: ['hero', 'story', 'highlights', 'contact'],
        }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.error || 'Generation failed');
      }

      setResult(data);
      setStep(3);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const previewHtml = result?.html_base64 
    ? atob(result.html_base64) 
    : '';

  return (
    <div className={styles.container}>
      {/* Header */}
      <header className={styles.header}>
        <div className={styles.headerContent}>
          <h1 className={styles.logo}>Personal IP Generator</h1>
          <p className={styles.tagline}>Create your personal IP website in minutes</p>
        </div>
      </header>

      {/* Progress */}
      <div className={styles.progress}>
        <div className={`${styles.progressStep} ${step >= 1 ? styles.active : ''}`}>
          <span className={styles.stepNumber}>1</span>
          <span className={styles.stepLabel}>Design</span>
        </div>
        <div className={styles.progressLine} />
        <div className={`${styles.progressStep} ${step >= 2 ? styles.active : ''}`}>
          <span className={styles.stepNumber}>2</span>
          <span className={styles.stepLabel}>Content</span>
        </div>
        <div className={styles.progressLine} />
        <div className={`${styles.progressStep} ${step >= 3 ? styles.active : ''}`}>
          <span className={styles.stepNumber}>3</span>
          <span className={styles.stepLabel}>Preview</span>
        </div>
      </div>

      {/* Step 1: Design Selection */}
      {step === 1 && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Choose Your Design</h2>
          <div className={styles.designGrid}>
            {designs.map(design => (
              <button
                key={design.id}
                className={`${styles.designCard} ${formData.design === design.id ? styles.selected : ''}`}
                onClick={() => setFormData(prev => ({ ...prev, design: design.id }))}
              >
                <div 
                  className={styles.designPreview}
                  style={{ 
                    backgroundColor: design.preview.bg,
                    color: design.preview.text,
                  }}
                >
                  <div className={styles.previewAccent} style={{ backgroundColor: design.preview.accent }} />
                  <div className={styles.previewText}>Aa</div>
                </div>
                <div className={styles.designInfo}>
                  <h3 className={styles.designName}>{design.name}</h3>
                  <p className={styles.designDesc}>{design.description}</p>
                </div>
              </button>
            ))}
          </div>
          <div className={styles.actions}>
            <button 
              className={styles.btnPrimary}
              onClick={() => setStep(2)}
            >
              Continue to Content
            </button>
          </div>
        </section>
      )}

      {/* Step 2: Content Form */}
      {step === 2 && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Tell Your Story</h2>
          <form className={styles.form} onSubmit={handleSubmit}>
            <div className={styles.formGrid}>
              <div className={styles.formGroup}>
                <label className={styles.label}>Your Name</label>
                <input
                  type="text"
                  name="name"
                  className={styles.input}
                  placeholder="李明"
                  value={formData.name}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>Your Role / Title</label>
                <input
                  type="text"
                  name="role"
                  className={styles.input}
                  placeholder="创业者 · 设计师 · 创作者"
                  value={formData.role}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>MBTI Type</label>
                <select
                  name="mbti"
                  className={styles.select}
                  value={formData.mbti}
                  onChange={handleInputChange}
                >
                  {mbtiTypes.map(mbti => (
                    <option key={mbti} value={mbti}>{mbti}</option>
                  ))}
                </select>
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>Short Bio</label>
                <input
                  type="text"
                  name="bio"
                  className={styles.input}
                  placeholder="一句话介绍你自己（150字内）"
                  value={formData.bio}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className={styles.formGroupFull}>
                <label className={styles.label}>Short Story (Hero Section)</label>
                <textarea
                  name="short_story"
                  className={styles.textarea}
                  placeholder="150-300字的短故事，用于首页展示..."
                  value={formData.short_story}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className={styles.formGroupFull}>
                <label className={styles.label}>Full Story (About Section)</label>
                <textarea
                  name="full_story"
                  className={styles.textareaLarge}
                  placeholder="400-800字的完整故事，关于你的经历、挑战和洞察..."
                  value={formData.full_story}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>Email</label>
                <input
                  type="email"
                  name="email"
                  className={styles.input}
                  placeholder="your@email.com"
                  value={formData.email}
                  onChange={handleInputChange}
                />
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>WeChat</label>
                <input
                  type="text"
                  name="wechat"
                  className={styles.input}
                  placeholder="your_wechat_id"
                  value={formData.wechat}
                  onChange={handleInputChange}
                />
              </div>

              <div className={styles.formGroup}>
                <label className={styles.label}>Personal Link</label>
                <input
                  type="url"
                  name="link"
                  className={styles.input}
                  placeholder="https://your-website.com"
                  value={formData.link}
                  onChange={handleInputChange}
                />
              </div>
            </div>

            {error && <p className={styles.error}>{error}</p>}

            <div className={styles.actions}>
              <button 
                type="button"
                className={styles.btnSecondary}
                onClick={() => setStep(1)}
              >
                Back
              </button>
              <button 
                type="submit"
                className={styles.btnPrimary}
                disabled={loading}
              >
                {loading ? 'Generating...' : 'Generate Website'}
              </button>
            </div>
          </form>
        </section>
      )}

      {/* Step 3: Preview */}
      {step === 3 && result && (
        <section className={styles.section}>
          <h2 className={styles.sectionTitle}>Your Website is Ready!</h2>
          <div className={styles.previewContainer}>
            <iframe
              srcDoc={previewHtml}
              className={styles.previewFrame}
              title="Website Preview"
            />
          </div>
          <div className={styles.actions}>
            <button 
              className={styles.btnSecondary}
              onClick={() => setStep(1)}
            >
              Start Over
            </button>
            <button 
              className={styles.btnPrimary}
              onClick={() => {
                const blob = new Blob([previewHtml], { type: 'text/html' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `${formData.name || 'website'}.html`;
                a.click();
                URL.revokeObjectURL(url);
              }}
            >
              Download HTML
            </button>
          </div>
        </section>
      )}

      {/* Footer */}
      <footer className={styles.footer}>
        <p>Powered by Diaolong Personal IP Generator</p>
      </footer>
    </div>
  );
}
