'use client';

import { useEffect, useRef, useState, useCallback } from 'react';
import React from 'react';
import styles from './page.module.css';
import * as pdfjsLib from 'pdfjs-dist';
import mammoth from 'mammoth';

// Configure pdf.js worker
pdfjsLib.GlobalWorkerOptions.workerSrc = `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjsLib.version}/pdf.worker.min.js`;

interface Dimension {
  icon: string;
  label: string;
  score: number;
  text: string;
}

interface AnalysisResult {
  dimensions: Dimension[];
  short_story: string;
  full_story: string;
  mbti: string;
}

interface DesignSystem {
  id: string;
  name: string;
  category: string;
  description: string;
  mood: string;
  recommended_for: string[];
  font_primary: string;
  preview?: { bg: string; text: string; accent: string };
  popularity: number;
}

const STATUS_LABELS = [
  '正在识别关键信息…', '蒸馏职业维度…', '提取核心技能…',
  '分析项目成就…', '梳理教育背景…', '洞察行业视野…',
  '刻画个人特质…', '评估发展潜力…', '生成叙事文本…'
];

const DIM_ICONS: Record<string, string> = {
  i1: '◎', i2: '◈', i3: '◉', i4: '△', i5: '◇', i6: '□', i7: '○'
};

export default function GeneratePage() {
  const [activeStep, setActiveStep] = useState(1);
  const [resumeText, setResumeText] = useState('');
  const [fileName, setFileName] = useState('');
  const [isExtracting, setIsExtracting] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analyzeIdx, setAnalyzeIdx] = useState(0);
  const [designSystems, setDesignSystems] = useState<DesignSystem[]>([]);
  const [selectedStyle, setSelectedStyle] = useState<string | null>(null);
  const [generatedHtml, setGeneratedHtml] = useState('');
  const [toastMsg, setToastMsg] = useState('');
  const [toastVisible, setToastVisible] = useState(false);

  const sectionRefs = [
    useRef<HTMLElement>(null),
    useRef<HTMLElement>(null),
    useRef<HTMLElement>(null),
    useRef<HTMLElement>(null),
  ];

  // Intersection observer for scroll-based stepper
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const stepNum = parseInt(entry.target.id.replace('section-step', ''));
          setActiveStep(stepNum);
        }
      });
    }, { threshold: 0.4 });

    sectionRefs.forEach(ref => {
      if (ref.current) observer.observe(ref.current);
    });

    return () => observer.disconnect();
  }, []);

  // Load design systems
  useEffect(() => {
    fetch('/api/designs')
      .then(r => r.json())
      .then(data => setDesignSystems(data.designs || []))
      .catch(() => {});
  }, []);

  const scrollToStep = useCallback((n: number) => {
    if (n < 1 || n > 4) return;
    const el = sectionRefs[n - 1]?.current;
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, []);

  const showToast = useCallback((msg: string) => {
    setToastMsg(msg);
    setToastVisible(true);
    setTimeout(() => setToastVisible(false), 2500);
  }, []);

  const canEnter = useCallback((n: number) => {
    if (n >= 2 && !resumeText.trim()) {
      showToast('请先上传文件或粘贴简历文本');
      return false;
    }
    if (n >= 4 && !selectedStyle) {
      showToast('请先选择一套视觉风格');
      return false;
    }
    return true;
  }, [resumeText, selectedStyle, showToast]);

  const handleAnalyze = useCallback(() => {
    if (!resumeText.trim()) {
      showToast('请先上传文件或粘贴简历文本');
      return;
    }
    if (activeStep === 1) scrollToStep(2);
    runAnalysis();
  }, [resumeText, activeStep, scrollToStep, showToast]);

  const runAnalysis = useCallback(async () => {
    if (isAnalyzing) return;
    setIsAnalyzing(true);
    setAnalyzeIdx(0);

    let idx = 0;
    const interval = setInterval(() => {
      idx = Math.min(idx + 1, STATUS_LABELS.length);
      setAnalyzeIdx(idx);
    }, 380);

    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: resumeText }),
      });

      if (!res.ok) throw new Error('Analysis failed');
      const data = await res.json();
      clearInterval(interval);
      setAnalysisResult(data);
    } catch {
      clearInterval(interval);
      showToast('解析失败，请重试');
    } finally {
      setIsAnalyzing(false);
    }
  }, [isAnalyzing, resumeText, showToast]);

  const handleGenerate = useCallback(async () => {
    if (!selectedStyle) {
      showToast('请先选择一套视觉风格');
      return;
    }

    if (!analysisResult) {
      showToast('请先完成AI解析');
      return;
    }

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          dimensions: analysisResult.dimensions,
          short_story: analysisResult.short_story,
          full_story: analysisResult.full_story,
          mbti: analysisResult.mbti,
          style: selectedStyle,
        }),
      });

      if (!res.ok) throw new Error('Generation failed');
      const data = await res.json();
      setGeneratedHtml(data.html || '');
      scrollToStep(4);
    } catch {
      showToast('生成失败，请重试');
    }
  }, [selectedStyle, analysisResult, scrollToStep, showToast]);

  const handleFileChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const ext = file.name.split('.').pop()?.toLowerCase() || '';
    if (!['pdf', 'docx', 'doc'].includes(ext)) {
      showToast('仅支持 PDF / DOCX / DOC 格式');
      return;
    }
    setFileName(file.name);
    setIsExtracting(true);

    const reader = new FileReader();
    reader.onload = async (event) => {
      try {
        const arrayBuffer = event.target?.result as ArrayBuffer;
        let text = '';

        if (ext === 'pdf') {
          const pdf = await pdfjsLib.getDocument({ data: arrayBuffer }).promise;
          const pageTexts: string[] = [];
          for (let i = 1; i <= pdf.numPages; i++) {
            const page = await pdf.getPage(i);
            const content = await page.getTextContent();
            const pageText = content.items
              .map((item: any) => item.str)
              .join(' ');
            pageTexts.push(pageText);
          }
          text = pageTexts.join('\n\n');
        } else if (ext === 'docx') {
          const result = await mammoth.extractRawText({ arrayBuffer });
          text = result.value;
        } else if (ext === 'doc') {
          // .doc is less commonly supported; mammoth can sometimes handle it
          const result = await mammoth.extractRawText({ arrayBuffer });
          text = result.value;
        }

        setResumeText(text);
        setIsExtracting(false);
        showToast(ext === 'pdf' ? 'PDF 文本已提取' : '文档文本已提取');
      } catch (err) {
        setIsExtracting(false);
        showToast('文件读取失败，请尝试粘贴文本');
      }
    };
    reader.onerror = () => {
      setIsExtracting(false);
      showToast('文件读取失败');
    };
    reader.readAsArrayBuffer(file);
  }, [showToast]);

  const selectedDesign = designSystems.find(s => s.id === selectedStyle);

  return (
    <div className={styles.page}>
      {/* NAV */}
      <nav className={styles.nav}>
        <div className={styles.navContainer}>
          <div className={styles.navLogo}>
            Personal <strong style={{ color: 'var(--accent)' }}>IP</strong> Site · 生成器
          </div>
          <div className={styles.navHint}>Step {activeStep} / 4</div>
        </div>
      </nav>

      {/* STEPPER */}
      <div className={styles.stepperSection}>
        <div className={styles.navContainer}>
          <div className={styles.stepper}>
            {[1, 2, 3, 4].map((step) => (
              <React.Fragment key={step}>
                <div
                  className={`${styles.stepItem} ${activeStep === step ? styles.active : ''} ${activeStep > step ? styles.done : ''}`}
                  onClick={() => {
                    if (step <= activeStep || canEnter(step)) scrollToStep(step);
                  }}
                >
                  <div className={styles.stepCircle}>
                    {activeStep > step ? '✓' : step}
                  </div>
                  <div className={styles.stepLabel}>
                    {['上传简历', 'AI 解析', '选择风格', '下载使用'][step - 1]}
                  </div>
                </div>
                {step < 4 && (
                  <div className={`${styles.stepArrow} ${activeStep > step ? styles.filled : ''}`}>
                    →
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>
        </div>
      </div>

      {/* STEP 1: UPLOAD */}
      <section className={styles.stepSection} id="section-step1" ref={sectionRefs[0]}>
        <div className={styles.container}>
          <p className={styles.sectionLabel}>STEP 1</p>
          <h2 className={styles.sectionTitle}>上传简历</h2>
          <p className={styles.sectionSubtitle}>上传 PDF 或 Word 文件，或直接在下方粘贴你的简历文本内容。</p>

          <div
            className={styles.uploadZone}
            onClick={() => document.getElementById('fileInput')?.click()}
          >
            <div className={styles.uploadIcon}>{isExtracting ? '⏳' : '↗'}</div>
            <div className={styles.uploadTitle}>
              {isExtracting ? '正在提取文本…' : '拖拽文件到此处，或点击上传'}
            </div>
            <div className={styles.uploadHint}>支持 PDF / DOCX / DOC，不超过 10MB</div>
            <div className={styles.uploadFormats}>
              <span className={styles.formatBadge}>.pdf</span>
              <span className={styles.formatBadge}>.docx</span>
              <span className={styles.formatBadge}>.doc</span>
            </div>
          </div>

          {fileName && (
            <div className={styles.fileCard}>
              <div className={styles.fileIconBadge}>
                {fileName.split('.').pop()?.toUpperCase()}
              </div>
              <div>
                <div className={styles.fileName}>{fileName}</div>
              </div>
              <button className={styles.fileRemove} onClick={() => setFileName('')}>×</button>
            </div>
          )}

          <div className={styles.uploadOr}>或者直接粘贴文本</div>

          <textarea
            className={styles.pasteBox}
            value={resumeText}
            onChange={e => setResumeText(e.target.value)}
            placeholder={`在此粘贴你的简历全文……\n\n示例：\n张三 | 高级前端工程师\n2019 — 2024  ABC 科技  前端技术负责人\n主导设计并落地了公司级组件库，覆盖 12 条业务线……`}
          />

          <div className={styles.stepActions}>
            <button
              className={`${styles.btn} ${styles.btnPrimary} ${styles.btnWide}`}
              onClick={handleAnalyze}
            >
              开始 AI 解析 →
            </button>
          </div>
        </div>
      </section>

      {/* STEP 2: ANALYSIS */}
      <section className={styles.stepSection} id="section-step2" ref={sectionRefs[1]}>
        <div className={styles.container}>
          <p className={styles.sectionLabel}>STEP 2</p>
          <h2 className={styles.sectionTitle}>AI 智能解析</h2>
          <p className={styles.sectionSubtitle}>从你的简历中蒸馏七大核心维度，生成叙事性内容。</p>

          {!analysisResult ? (
            <div className={styles.analysisStatus}>
              <div className={styles.pulse} />
              <div className={styles.dots}>
                <span />
                <span />
                <span />
              </div>
              <div className={styles.statusText}>
                {STATUS_LABELS[Math.min(analyzeIdx, STATUS_LABELS.length - 1)]}
              </div>
            </div>
          ) : (
            <div className={styles.dimensionsGrid}>
              {analysisResult.dimensions.map((dim, i) => (
                <div key={i} className={styles.dimCard}>
                  <div className={styles.dimHeader}>
                    <div className={`${styles.dimIcon} ${styles[`i${i + 1}` as keyof typeof styles]}`}>
                      {DIM_ICONS[`i${i + 1}`]}
                    </div>
                    <div className={styles.dimLabel}>{dim.label}</div>
                    <div className={styles.dimScore}>{dim.score}</div>
                  </div>
                  <div className={styles.dimText}>{dim.text}</div>
                </div>
              ))}
            </div>
          )}

          {analysisResult && (
            <div className={`${styles.stepActions} ${styles.right}`}>
              <button
                className={`${styles.btn} ${styles.btnSecondary}`}
                onClick={() => scrollToStep(1)}
              >
                ← 返回修改
              </button>
              <button
                className={`${styles.btn} ${styles.btnPrimary}`}
                onClick={() => scrollToStep(3)}
              >
                选择视觉风格 →
              </button>
            </div>
          )}
        </div>
      </section>

      {/* STEP 3: STYLE SELECTION */}
      <section className={styles.stepSection} id="section-step3" ref={sectionRefs[2]}>
        <div className={styles.container}>
          <p className={styles.sectionLabel}>STEP 3</p>
          <h2 className={styles.sectionTitle}>选择视觉风格</h2>
          <p className={styles.sectionSubtitle}>
            从 {designSystems.length || 54} 套设计系统中选择适配风格，实时预览页面效果。
          </p>

          <div className={styles.stylesGrid}>
            {designSystems.slice(0, 30).map(sys => (
              <div
                key={sys.id}
                className={`${styles.styleCard} ${selectedStyle === sys.id ? styles.selected : ''}`}
                onClick={() => setSelectedStyle(sys.id)}
              >
                <div
                  className={styles.styleThumb}
                  style={{
                    background: sys.preview?.bg || '#ffffff',
                    color: sys.preview?.text || '#000000',
                  }}
                >
                  <span>{sys.name}</span>
                </div>
                <div className={styles.styleTitle}>{sys.name}</div>
                <div className={styles.styleCheck}>✓</div>
              </div>
            ))}
          </div>

          {selectedStyle && (
            <div className={styles.previewFrame}>
              <div className={styles.previewBar}>
                <div className={styles.previewDots}>
                  <span />
                  <span />
                  <span />
                </div>
                <div className={styles.previewUrl}>your-name.personal-site.com</div>
              </div>
              <div
                className={styles.previewBody}
                style={{
                  background: selectedDesign?.preview?.bg || '#ffffff',
                  color: selectedDesign?.preview?.text || '#000000',
                }}
              >
                <div style={{ maxWidth: 600 }}>
                  <h1 style={{ marginBottom: 4, fontSize: '1.5rem', fontWeight: 600 }}>
                    {analysisResult?.short_story?.split('，')[0] || '你的名字'}
                  </h1>
                  <p style={{ marginBottom: 16, fontSize: '0.9rem', opacity: 0.8 }}>
                    {selectedDesign?.mood || selectedDesign?.description}
                  </p>
                  <p style={{ lineHeight: 1.75, fontSize: '0.88rem' }}>
                    {analysisResult?.full_story || '你的故事将显示在这里'}
                  </p>
                </div>
              </div>
            </div>
          )}

          <div className={`${styles.stepActions} ${styles.right}`}>
            <button
              className={`${styles.btn} ${styles.btnSecondary}`}
              onClick={() => scrollToStep(2)}
            >
              ← 返回修改
            </button>
            <button
              className={`${styles.btn} ${styles.btnPrimary}`}
              onClick={handleGenerate}
            >
              生成完整页面 →
            </button>
          </div>
        </div>
      </section>

      {/* STEP 4: DOWNLOAD */}
      <section className={styles.stepSection} id="section-step4" ref={sectionRefs[3]}>
        <div className={styles.container}>
          <p className={styles.sectionLabel}>STEP 4</p>
          <h2 className={styles.sectionTitle}>预览与下载</h2>
          <p className={styles.sectionSubtitle}>
            你的个人站点已生成。预览确认后，点击下载完整 HTML 文件。
          </p>

          <div className={styles.dlFrame}>
            <div className={styles.dlBar}>
              <div className={styles.previewDots}>
                <span />
                <span />
                <span />
              </div>
            </div>
            <div
              className={styles.dlBody}
              style={{
                background: selectedDesign?.preview?.bg || '#ffffff',
                color: selectedDesign?.preview?.text || '#000000',
              }}
              dangerouslySetInnerHTML={{
                __html: generatedHtml || `
                  <div style="max-width:680px;margin:0 auto;padding:24px">
                    <h1 style="font-size:1.8rem;margin-bottom:8px">预览区域</h1>
                    <p style="margin-bottom:24px">点击"生成完整页面"后在此处预览</p>
                  </div>
                `,
              }}
            />
          </div>

          <div className={`${styles.stepActions} ${styles.centered}`}>
            <button
              className={`${styles.btn} ${styles.btnSecondary}`}
              onClick={() => scrollToStep(3)}
            >
              ← 更换风格
            </button>
            {generatedHtml && (
              <button
                className={`${styles.btn} ${styles.btnPrimary}`}
                onClick={() => {
                  const blob = new Blob([generatedHtml], { type: 'text/html' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = 'personal-ip-site.html';
                  a.click();
                  URL.revokeObjectURL(url);
                }}
              >
                下载 HTML 文件
              </button>
            )}
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className={styles.footer}>
        <div className={styles.container}>
          <p>Personal IP Site Generator · Diaolong 叙事工程 驱动</p>
        </div>
      </footer>

      {/* TOAST */}
      <div className={`${styles.toast} ${toastVisible ? styles.show : ''}`}>{toastMsg}</div>
    </div>
  );
}