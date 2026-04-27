import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Upload, 
  Activity, 
  Play, 
  Pause, 
  CheckCircle2, 
  AlertCircle, 
  History,
  Heart,
  FileAudio,
  ChevronRight,
  RefreshCw
} from 'lucide-react';
import './index.css';

// --- Mock API ---
const analyzeHeartSound = async (file) => {
  // Simulating API call
  await new Promise(resolve => setTimeout(resolve, 2500));
  const prob = Math.random();
  return {
    prediction: prob > 0.5 ? "Murmur" : "Normal",
    probability: prob
  };
};

function App() {
  const [file, setFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);
  const [audioUrl, setAudioUrl] = useState(null);

  const handleFileUpload = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'audio/wav') {
      setFile(selectedFile);
      setResult(null);
      if (audioUrl) URL.revokeObjectURL(audioUrl);
      setAudioUrl(URL.createObjectURL(selectedFile));
    } else {
      alert("Please upload a valid .wav file");
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    setAnalyzing(true);
    try {
      const data = await analyzeHeartSound(file);
      setResult(data);
      const newHistoryItem = {
        id: Date.now(),
        fileName: file.name,
        prediction: data.prediction,
        probability: data.probability,
        timestamp: new Date().toLocaleTimeString()
      };
      setHistory(prev => [newHistoryItem, ...prev].slice(0, 5));
    } catch (error) {
      console.error("Analysis failed", error);
    } finally {
      setAnalyzing(false);
    }
  };

  const togglePlay = () => {
    if (audioRef.current) {
      if (isPlaying) audioRef.current.pause();
      else audioRef.current.play();
      setIsPlaying(!isPlaying);
    }
  };

  const getRiskLevel = (prob) => {
    if (prob < 0.45) return { label: 'Low Risk', color: 'var(--success)', class: 'risk-low' };
    if (prob <= 0.60) return { label: 'Moderate Risk', color: 'var(--warning)', class: 'risk-mod' };
    return { label: 'High Risk', color: 'var(--danger)', class: 'risk-high' };
  };

  return (
    <div className="container">
      {/* Header */}
      <header style={{ marginBottom: '3rem', marginTop: '1rem' }}>
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}
        >
          <div className="glass" style={{ padding: '0.75rem', borderRadius: '16px' }}>
            <Heart color="var(--primary)" size={32} fill="var(--primary-glow)" />
          </div>
          <div>
            <h1 className="title-gradient" style={{ fontSize: '1.8rem' }}>Heart Murmur AI</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Advanced Cardiovascular Screening</p>
          </div>
        </motion.div>
      </header>

      <main style={{ display: 'grid', gridTemplateColumns: result ? '1fr 1fr' : '1fr', gap: '2rem', transition: 'all 0.5s ease' }}>
        
        {/* Left Column: Upload & Player */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <motion.div 
            layout
            className="glass"
            style={{ padding: '2.5rem' }}
          >
            <h2 style={{ marginBottom: '1.5rem', fontSize: '1.25rem' }}>Heart Sound Upload</h2>
            
            {!file ? (
              <div 
                className="upload-zone"
                onDragOver={(e) => e.preventDefault()}
                onDrop={(e) => {
                  e.preventDefault();
                  const droppedFile = e.dataTransfer.files[0];
                  if (droppedFile.type === 'audio/wav') {
                    setFile(droppedFile);
                    setAudioUrl(URL.createObjectURL(droppedFile));
                  }
                }}
              >
                <input 
                  type="file" 
                  accept=".wav" 
                  id="file-upload" 
                  hidden 
                  onChange={handleFileUpload} 
                />
                <label htmlFor="file-upload" style={{ cursor: 'pointer', textAlign: 'center' }}>
                  <motion.div
                    whileHover={{ scale: 1.05 }}
                    style={{ marginBottom: '1rem' }}
                  >
                    <Upload size={48} color="var(--primary)" style={{ opacity: 0.8 }} />
                  </motion.div>
                  <p style={{ fontWeight: '500' }}>Drag & drop your .wav file</p>
                  <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.5rem' }}>or click to browse your files</p>
                </label>
              </div>
            ) : (
              <div className="file-active">
                <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', background: 'rgba(255,255,255,0.03)', padding: '1rem', borderRadius: '12px', border: '1px solid var(--glass-border)' }}>
                  <FileAudio color="var(--primary)" />
                  <div style={{ overflow: 'hidden' }}>
                    <p style={{ fontWeight: '500', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{file.name}</p>
                    <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{(file.size / 1024 / 1024).toFixed(2)} MB • Ready to analyze</p>
                  </div>
                  <button 
                    onClick={() => {setFile(null); setResult(null);}} 
                    style={{ marginLeft: 'auto', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}
                  >
                    Change
                  </button>
                </div>

                <div className="audio-player glass" style={{ marginTop: '1.5rem', padding: '1rem', borderRadius: '16px', overflow: 'hidden' }}>
                  <audio ref={audioRef} src={audioUrl} onEnded={() => setIsPlaying(false)} />
                  <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', marginBottom: '1rem' }}>
                    <button onClick={togglePlay} className="play-button">
                      {isPlaying ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" />}
                    </button>
                    <div style={{ flex: 1 }}>
                      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '4px' }}>Waveform Analysis</p>
                      <div className="visualizer-mock">
                        {[...Array(32)].map((_, i) => (
                          <div 
                            key={i} 
                            className="bar" 
                            style={{ 
                              height: isPlaying ? `${20 + Math.random() * 80}%` : '20%',
                              transition: 'height 0.15s ease',
                              animation: isPlaying ? 'wave 1s infinite ease-in-out' : 'none',
                              animationDelay: `${i * 0.03}s`
                            }} 
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                  
                  {/* Spectrogram Mock */}
                  <div style={{ background: 'rgba(0,0,0,0.2)', height: '60px', borderRadius: '8px', border: '1px solid var(--glass-border)', position: 'relative', overflow: 'hidden' }}>
                    <div className="spectrogram-scroll" style={{ animationPlayState: isPlaying ? 'running' : 'paused' }}></div>
                    <div style={{ position: 'absolute', top: '5px', left: '10px', fontSize: '0.65rem', color: 'var(--primary)', opacity: 0.6, fontWeight: '700' }}>SPECTROGRAM</div>
                  </div>
                </div>

                <button 
                  className="button-primary" 
                  style={{ width: '100%', marginTop: '1.5rem', justifyContent: 'center', height: '56px' }}
                  onClick={handleAnalyze}
                  disabled={analyzing}
                >
                  {analyzing ? (
                    <>
                      <RefreshCw className="spinner" size={20} />
                      Processing Audio...
                    </>
                  ) : (
                    <>
                      <Activity size={20} />
                      Analyze Heart Sound
                    </>
                  )}
                </button>
              </div>
            )}
          </motion.div>

          {/* History Section */}
          <motion.div className="glass" style={{ padding: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
              <History size={18} color="var(--text-muted)" />
              <h3 style={{ fontSize: '1rem', color: 'var(--text-muted)' }}>Recent History</h3>
            </div>
            {history.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', fontStyle: 'italic' }}>No recent predictions</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {history.map(item => (
                  <div key={item.id} className="history-item">
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                      <span style={{ fontWeight: '500', fontSize: '0.85rem' }}>{item.prediction}</span>
                      <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{item.timestamp}</span>
                    </div>
                    <div className="history-bar-bg">
                      <div className="history-bar-fill" style={{ width: `${item.probability * 100}%`, background: getRiskLevel(item.probability).color }} />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        </div>

        {/* Right Column: Results */}
        <AnimatePresence mode="wait">
          {analyzing ? (
            <motion.div 
              key="loading"
              initial={{ opacity: 0, scale: 0.95 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="glass result-container"
              style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '2rem', padding: '3rem' }}
            >
              <div className="pulse-container">
                <div className="pulse-ring"></div>
                <div className="pulse-heart">
                  <Activity size={48} color="var(--primary)" />
                </div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <h2 style={{ marginBottom: '0.5rem' }}>Analyzing Signal</h2>
                <p style={{ color: 'var(--text-muted)' }}>Our AI is processing the cardiac waveform to detect irregularities...</p>
              </div>
            </motion.div>
          ) : result ? (
            <motion.div 
              key="result"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="glass result-container"
              style={{ padding: '2.5rem' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
                <div>
                  <span style={{ 
                    background: getRiskLevel(result.probability).color + '20', 
                    color: getRiskLevel(result.probability).color,
                    padding: '0.4rem 0.8rem',
                    borderRadius: '20px',
                    fontSize: '0.75rem',
                    fontWeight: '700',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em'
                  }}>
                    {getRiskLevel(result.probability).label}
                  </span>
                  <h2 style={{ fontSize: '2.5rem', marginTop: '1rem', fontWeight: '800' }}>
                    {result.prediction}
                  </h2>
                </div>
                <div className="circular-progress">
                  <svg width="80" height="80">
                    <circle cx="40" cy="40" r="34" className="circular-bg" />
                    <circle 
                      cx="40" cy="40" r="34" 
                      className="circular-fill" 
                      style={{ 
                        strokeDashoffset: 213.6 * (1 - result.probability),
                        stroke: getRiskLevel(result.probability).color
                      }} 
                    />
                  </svg>
                  <div className="circular-text">
                    {Math.round(result.probability * 100)}%
                  </div>
                </div>
              </div>

              <div style={{ marginBottom: '2rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
                  <span style={{ fontWeight: '600' }}>Confidence Score</span>
                  <span style={{ color: 'var(--text-muted)' }}>{(result.probability * 100).toFixed(1)}%</span>
                </div>
                <div className="progress-bg">
                  <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: `${result.probability * 100}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className="progress-fill"
                    style={{ background: getRiskLevel(result.probability).color }}
                  />
                </div>
              </div>

              <div className="result-info-card">
                <div style={{ display: 'flex', gap: '1rem' }}>
                  {result.prediction === 'Normal' ? (
                    <CheckCircle2 color="var(--success)" size={24} />
                  ) : (
                    <AlertCircle color="var(--danger)" size={24} />
                  )}
                  <div>
                    <h4 style={{ marginBottom: '0.25rem' }}>Clinical Assessment</h4>
                    <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                      {result.prediction === 'Normal' 
                        ? "The heart sound signal matches the profile of a healthy heart rhythm. No significant murmurs or irregularities were detected."
                        : "Potential cardiac irregularities detected. The signal shows patterns consistent with heart murmurs. We recommend a clinical evaluation."
                      }
                    </p>
                  </div>
                </div>
              </div>

              <button 
                className="button-secondary"
                style={{ width: '100%', marginTop: '2rem' }}
                onClick={() => {setResult(null); setFile(null);}}
              >
                New Screening
              </button>
            </motion.div>
          ) : (
             <div className="glass empty-result" style={{ padding: '3rem', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: 0.5 }}>
               <Activity size={64} style={{ marginBottom: '1.5rem', opacity: 0.2 }} />
               <h3>Awaiting Analysis</h3>
               <p>Upload a heart sound file to see results here</p>
             </div>
          )}
        </AnimatePresence>
      </main>

      <footer style={{ marginTop: '3rem', paddingBottom: '2rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.8rem' }}>
        <p>© 2026 CardiacAI Solutions. For screening purposes only. Always consult a medical professional.</p>
      </footer>

      <style>{`
        .upload-zone {
          border: 2px dashed var(--glass-border);
          border-radius: 16px;
          padding: 3rem;
          display: flex;
          flex-direction: column;
          align-items: center;
          transition: all 0.3s ease;
        }
        .upload-zone:hover {
          border-color: var(--primary);
          background: rgba(56, 189, 248, 0.02);
        }
        .play-button {
          background: var(--primary);
          color: var(--bg-darker);
          border: none;
          width: 48px;
          height: 48px;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: transform 0.2s;
        }
        .play-button:hover { transform: scale(1.1); }
        .visualizer-mock {
          display: flex;
          align-items: center;
          gap: 3px;
          height: 40px;
          flex: 1;
        }
        .bar {
          flex: 1;
          background: var(--primary);
          opacity: 0.6;
          border-radius: 10px;
          min-height: 4px;
        }
        .spinner { animation: spin 1s linear infinite; }
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        
        .progress-bg { height: 12px; background: rgba(255,255,255,0.05); border-radius: 10px; overflow: hidden; }
        .progress-fill { height: 100%; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.2); }
        
        .circular-progress { position: relative; width: 80px; height: 80px; }
        .circular-bg { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 6; }
        .circular-fill { fill: none; stroke-width: 6; stroke-linecap: round; transform: rotate(-90deg); transform-origin: 50% 50%; stroke-dasharray: 213.6; transition: stroke-dashoffset 1s ease; }
        .circular-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-weight: 700; font-size: 1.1rem; }
        
        .result-info-card { background: rgba(255,255,255,0.02); border: 1px solid var(--glass-border); border-radius: 16px; padding: 1.25rem; margin-top: 1rem; }
        .button-secondary { background: transparent; border: 1px solid var(--glass-border); color: var(--text-main); padding: 0.8rem; border-radius: 12px; font-weight: 600; cursor: pointer; transition: all 0.3s; }
        .button-secondary:hover { background: rgba(255,255,255,0.05); }

        .history-item { margin-bottom: 0.5rem; }
        .history-bar-bg { height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px; }
        .history-bar-fill { height: 100%; border-radius: 2px; }

        .pulse-container { position: relative; width: 120px; height: 120px; display: flex; align-items: center; justify-content: center; }
        .pulse-ring { position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 4px solid var(--primary); animation: pulse-glow 2s infinite; }
        .pulse-heart { position: relative; z-index: 1; }

        .spectrogram-scroll {
          position: absolute;
          top: 0; left: 0;
          width: 200%; height: 100%;
          background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(56, 189, 248, 0.1) 10%, 
            rgba(56, 189, 248, 0.2) 20%, 
            rgba(56, 189, 248, 0.05) 30%,
            transparent 40%,
            rgba(56, 189, 248, 0.15) 50%,
            rgba(56, 189, 248, 0.05) 60%
          );
          background-size: 50% 100%;
          animation: scroll 4s linear infinite;
        }
        @keyframes scroll {
          from { transform: translateX(0); }
          to { transform: translateX(-50%); }
        }

        @media (max-width: 768px) {
          main { grid-template-columns: 1fr !important; }
        }
      `}</style>
    </div>
  );
}

export default App;
