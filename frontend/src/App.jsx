import { useEffect, useRef, useState } from 'react';
import ScoreRing from './ScoreRing';

const DOMAIN_FLEET = [
  { name: 'agenticauditai.digital', role: 'Primary Platform', active: true },
  { name: 'agenticauditai.site', role: 'Mirror Portal', active: true },
  { name: 'humanorai.live', role: 'Turing Live Engine', active: true },
  { name: 'aiquizgame.live', role: 'Gamified Benchmarks', active: true },
  { name: 'paygig.click', role: 'Monetization API', active: true },
];

const playSynthesizedAudio = (type) => {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    if (type === 'DENY') {
      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(160, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(40, ctx.currentTime + 0.3);
      gain.gain.setValueAtTime(0.32, ctx.currentTime);
      osc.start();
      osc.stop(ctx.currentTime + 0.3);
    } else if (type === 'ALLOW') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.2);
      gain.gain.setValueAtTime(0.2, ctx.currentTime);
      osc.start();
      osc.stop(ctx.currentTime + 0.2);
    } else {
      osc.type = 'square';
      osc.frequency.setValueAtTime(700, ctx.currentTime);
      gain.gain.setValueAtTime(0.05, ctx.currentTime);
      osc.start();
      osc.stop(ctx.currentTime + 0.05);
    }
  } catch (e) {
    // Audio context may not be available in all browsers.
  }
};

function App() {
  const [messages, setMessages] = useState([]);
  const [patches, setPatches] = useState([]);
  const [score, setScore] = useState(100);
  const [status, setStatus] = useState('SYSTEM READY');
  const [lastAction, setLastAction] = useState('IDLE');
  const ws = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const wsUrl = 'ws://localhost:8000/ws';
    ws.current = new WebSocket(wsUrl);

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'MESSAGE') {
        setMessages((prev) => [...prev, data]);
        setLastAction(data.action || 'PROCESS');
        if (data.score !== undefined) {
          setScore(data.score);
        }
        if (data.action) {
          playSynthesizedAudio(data.action);
        } else {
          playSynthesizedAudio('TICK');
        }
      } else if (data.type === 'RAG_PATCH') {
        setPatches((prev) => [...prev, data]);
      } else if (data.type === 'STATUS') {
        setStatus(data.text);
      } else if (data.type === 'SYSTEM') {
        setStatus(data.text);
      }
    };

    ws.current.onopen = () => {
      setStatus('CONNECTED');
    };

    ws.current.onclose = () => {
      setStatus('DISCONNECTED');
    };

    return () => ws.current && ws.current.close();
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth', block: 'end' });
    }
  }, [messages]);

  const triggerAuditSequence = () => {
    setMessages([]);
    setPatches([]);
    setScore(100);
    setStatus('ARMING ADVERSARIAL AGENTS...');
    if (ws.current) {
      ws.current.send(JSON.stringify({ command: 'START_AUDIT' }));
    }
  };

  const downloadReport = (fmt) => {
    window.open(`http://localhost:8000/api/download-report?fmt=${fmt}`, '_blank');
  };

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      <header className="topbar">
        <div>
          <h1 className="hero-title">AGENTIC AUDIT AI</h1>
          <div className="hero-subtitle">OPERATOR: katelynn@kalib • HOST: agenticauditai.digital</div>
        </div>
        <div className="hero-status">
          <ScoreRing score={score} />
          <div>
            <div className="status-pill">{status}</div>
            <div className="substatus-pill">ACTION: {lastAction}</div>
          </div>
        </div>
      </header>

      <section style={{ margin: '24px 0', display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
        {DOMAIN_FLEET.map((d, i) => (
          <span key={i} className="domain-pill">
            ● {d.name} <span style={{ color: '#6b7280' }}>({d.role})</span>
          </span>
        ))}
      </section>

      <section className="action-bar">
        <button onClick={triggerAuditSequence} className="cyber-button">INITIALIZE ADVERSARIAL FIGHT CLUB</button>
        <button onClick={() => downloadReport('md')} className="ghost-button">DOWNLOAD MARKDOWN REPORT</button>
        <button onClick={() => downloadReport('pdf')} className="ghost-button">EXPORT CERTIFIED PDF</button>
      </section>

      <main style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '20px', alignItems: 'start' }}>
        <div style={{ background: '#0c0f18', border: '1px solid #1f2937', borderRadius: '18px', padding: '20px', minHeight: '520px' }}>
          <h3 style={{ color: '#00f0ff', marginBottom: '16px' }}>LIVE TRANSMISSION FEED</h3>
          <div style={{ display: 'grid', gap: '16px' }}>
            {messages.map((m, idx) => (
              <div key={idx} className={`message-card ${m.action === 'DENY' ? 'deny' : m.action === 'ALLOW' ? 'allow' : ''}`}>
                <div className="message-header">
                  <span>{m.agent.toUpperCase()} • ROUND {m.round}</span>
                  {m.entropy !== undefined && <span>ENTROPY {m.entropy}</span>}
                </div>
                <div className="message-body">{m.text}</div>
                {m.action && <div className="message-badge"><span>{m.action}</span></div>}
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
        </div>

        <div style={{ display: 'grid', gap: '18px' }}>
          <div className="status-card">
            <h3>DYNAMIC RAG PATCH FEED</h3>
            <div style={{ display: 'grid', gap: '12px' }}>
              {patches.length === 0 && <div style={{ color: '#94a3b8' }}>No patches injected yet. Run the simulation to generate hardened policy updates.</div>}
              {patches.map((p, idx) => (
                <div key={idx} style={{ background: '#111420', borderRadius: '12px', padding: '14px', border: '1px solid #1f2937' }}>
                  <div style={{ color: '#c7d2fe', fontSize: '0.85rem', marginBottom: '8px' }}>PATCH #{idx + 1}</div>
                  <div style={{ color: '#d1d5db', lineHeight: 1.6 }}>{p.patch}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="status-card">
            <h3>TACTICAL OVERVIEW</h3>
            <div className="overview-row"><span>Messages</span><strong>{messages.length}</strong></div>
            <div className="overview-row"><span>Patches</span><strong>{patches.length}</strong></div>
            <div className="overview-row"><span>Threat Level</span><strong>{100 - score}%</strong></div>
            <div className="overview-meter">
              <div className="overview-meter__fill" style={{ width: `${100 - score}%` }} />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
