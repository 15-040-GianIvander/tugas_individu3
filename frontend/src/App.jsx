import React, { useEffect, useState, useRef } from "react";
import axios from "axios";

const API_BASE = "http://localhost:8000";

function Toast({ toasts, removeToast }) {
  return (
    <div className="toasts" aria-live="polite">
      {toasts.map(t => (
        <div key={t.id} className={`toast ${t.type || "info"}`}>
          <div className="toast-content">
            <strong>{t.title}</strong>
            <div className="toast-msg">{t.message}</div>
          </div>
          <button className="toast-close" onClick={() => removeToast(t.id)}>✕</button>
        </div>
      ))}
    </div>
  );
}

function Spinner({ size = 18 }) {
  return <div className="spinner" style={{ width: size, height: size }} aria-hidden />;
}

function SentimentPill({ sentiment }) {
  const cls = sentiment === "positive" ? "pill positive"
    : sentiment === "negative" ? "pill negative"
    : sentiment === "neutral" ? "pill neutral"
    : "pill unknown";
  return <span className={cls}>{sentiment || "unknown"}</span>;
}

export default function App() {
  const [text, setText] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [fetching, setFetching] = useState(false);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState("");
  const [toasts, setToasts] = useState([]);
  const nextToastId = useRef(1);

  useEffect(() => {
    loadReviews();
  }, []);

  function addToast(title, message, type = "info", timeout = 4000) {
    const id = nextToastId.current++;
    setToasts(prev => [...prev, { id, title, message, type }]);
    if (timeout) setTimeout(() => removeToast(id), timeout);
  }
  function removeToast(id) {
    setToasts(prev => prev.filter(t => t.id !== id));
  }

  async function loadReviews() {
    setFetching(true);
    setError(null);
    try {
      const res = await axios.get(`${API_BASE}/api/reviews`);
      setResults(res.data || []);
    } catch (err) {
      console.error(err);
      setError("Gagal mengambil reviews. Cek backend.");
      addToast("Error", "Gagal ambil reviews dari server", "error");
    } finally {
      setFetching(false);
    }
  }

  // optimistic analyze: show pending card, then replace
  async function handleAnalyze(e) {
    e?.preventDefault();
    setError(null);
    if (!text.trim()) {
      setError("Tolong isi review dulu.");
      addToast("Oops", "Tolong isi review dulu.", "error");
      return;
    }

    // create optimistic item
    const tempId = `temp-${Date.now()}`;
    const optimistic = {
      id: tempId,
      text,
      sentiment: "pending",
      key_points: "Pending…",
      __optimistic: true,
    };
    setResults(prev => [optimistic, ...prev]);
    setText("");
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/api/analyze-review`, { text }, { headers: { "Content-Type": "application/json" } });
      // replace optimistic item with real response (match by tempId)
      setResults(prev => prev.map(r => (r.id === tempId ? res.data : r)));
      addToast("Sukses", "Review berhasil dianalisis dan disimpan.", "success");
    } catch (err) {
      console.error(err);
      // remove optimistic item and show error
      setResults(prev => prev.filter(r => r.id !== tempId));
      const msg = err?.response?.data?.detail || "Gagal menganalisis review.";
      setError(msg);
      addToast("Error", msg, "error", 6000);
    } finally {
      setLoading(false);
    }
  }

  function handleCopyKeypoints(text) {
    navigator.clipboard?.writeText(text).then(() => {
      addToast("Copied", "Key points disalin ke clipboard", "success");
    }).catch(() => {
      addToast("Gagal", "Tidak bisa menyalin ke clipboard", "error");
    });
  }

  const filtered = results.filter(r => {
    if (!filter.trim()) return true;
    return (r.text || "").toLowerCase().includes(filter.toLowerCase());
  });

  return (
    <div className="app">
      <Toast toasts={toasts} removeToast={removeToast} />

      <header className="hero">
        <div className="hero-left">
          <h1>Product Review <span className="accent">Analyzer</span></h1>
          <p className="sub">Analisis otomatis sentiment & ekstraksi poin penting — cepat & rapi.</p>
        </div>
        <div className="hero-right">
          <button className="btn ghost" onClick={loadReviews} disabled={fetching}>
            {fetching ? (<><Spinner /> Refreshing</>) : "Refresh"}
          </button>
        </div>
      </header>

      <main className="container">
        <section className="panel">
          <form onSubmit={handleAnalyze} className="form">
            <textarea
              placeholder="Tulis review produk di sini..."
              value={text}
              onChange={e => setText(e.target.value)}
              rows={4}
              aria-label="review-text"
              disabled={loading}
            />
            <div className="controls">
              <div className="left-controls">
                <button className="btn primary" type="submit" disabled={loading}>{loading ? <><Spinner /> Analyzing...</> : "Analyze"}</button>
                <button type="button" className="btn secondary" onClick={() => { setText(""); setError(null); }}>Clear</button>
              </div>

              <div className="right-controls">
                <input className="search" placeholder="Search results..." value={filter} onChange={e => setFilter(e.target.value)} />
              </div>
            </div>
            {error && <div className="form-error">{error}</div>}
          </form>
        </section>

        <section className="results-panel">
          <div className="results-meta">
            <h2>Results</h2>
            <div className="meta-right">
              <small>{filtered.length} item</small>
            </div>
          </div>

          <div className="grid">
            {filtered.map(r => (
              <article key={r.id || Math.random()} className={`card ${r.__optimistic ? "optimistic" : ""}`}>
                <div className="card-head">
                  <div className="card-title">{r.text}</div>
                  <div className="card-info">
                    <SentimentPill sentiment={r.sentiment} />
                    <small className="card-id">id: {String(r.id).startsWith("temp-") ? "…" : r.id}</small>
                  </div>
                </div>

                <div className="card-body">
                  {r.sentiment === "pending" ? (
                    <div className="pending-row"><Spinner size={16}/> Processing…</div>
                  ) : (
                    <pre className="keypoints">{r.key_points}</pre>
                  )}
                </div>

                <div className="card-actions">
                  <button className="link" onClick={() => handleCopyKeypoints(r.key_points)}>Copy key points</button>
                  <a className="link" href="#" onClick={(e)=>{ e.preventDefault(); addToast("Info", `Review: ${r.text.slice(0,60)}`, "info");}}>Info</a>
                </div>
              </article>
            ))}
            {filtered.length === 0 && <div className="empty-state">No reviews yet — coba tambah review!</div>}
          </div>
        </section>
      </main>

      <footer className="footer">
        <small>Built with ❤️ — Product Review Analyzer</small>
      </footer>
    </div>
  );
}
