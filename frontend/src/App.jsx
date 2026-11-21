import { useState, useEffect } from "react";
import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5001";

const pretty = (s) => s.replace(/_/g, " ");


const QUICK_PICKS = ["high_fever", "headache", "cough", "fatigue", "vomiting", "itching"];

function App() {
  const [allSymptoms, setAllSymptoms] = useState([]); 
  const [query, setQuery] = useState("");             
  const [selected, setSelected] = useState([]);       
  const [result, setResult] = useState(null);         
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  useEffect(() => {
    axios
      .get(`${API_URL}/symptoms`)
      .then((res) => setAllSymptoms(res.data))
      .catch(() => setError("Cannot reach the server. Is the backend running?"));
  }, []);


  const matches = query.trim()
    ? allSymptoms
        .filter((s) => pretty(s).includes(query.toLowerCase()) && !selected.includes(s))
        .slice(0, 6)
    : [];

  const quickPicks = QUICK_PICKS.filter(
    (s) => allSymptoms.includes(s) && !selected.includes(s)
  );

  const addSymptom = (s) => {
    setSelected([...selected, s]);
    setQuery("");
    setError("");
  };

  const removeSymptom = (s) => {
    setSelected(selected.filter((x) => x !== s));
  };


  const handleKeyDown = (e) => {
    if (e.key === "Enter" && matches.length > 0) addSymptom(matches[0]);
  };

  const handlePredict = async () => {
    if (selected.length === 0) {
      setError("Please select at least one symptom.");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/predict`, { symptoms: selected });
      setResult(res.data);
    } catch (err) {
      setResult(null);
      setError("Something went wrong. Please try again.");
    }
    setLoading(false);
  };

  const handleReset = () => {
    setSelected([]);
    setQuery("");
    setResult(null);
    setError("");
  };

  return (
    <div className="page">
      <header className="hero">
        <div className="logo" >🩺</div>
        <h1>Disease Prediction</h1>
        <p>Pick your symptoms and get a possible prediction, powered by machine learning.</p>
      </header>

      <main className="card">
        <label className="label">1. Search and add your symptoms</label>

        <div className="search-wrap">
          <span className="search-icon">🔍</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type a symptom, e.g. fever, headache..."
          />
          {matches.length > 0 && (
            <ul className="dropdown">
              {matches.map((s) => (
                <li key={s} onClick={() => addSymptom(s)}>
                  <span>+</span> {pretty(s)}
                </li>
              ))}
            </ul>
          )}
        </div>

        {quickPicks.length > 0 && (
          <div className="quick">
            <span className="quick-title">Common:</span>
            {quickPicks.map((s) => (
              <button key={s} className="quick-btn" onClick={() => addSymptom(s)}>
                {pretty(s)}
              </button>
            ))}
          </div>
        )}

        <label className="label">
          2. Selected symptoms <span className="count">{selected.length}</span>
        </label>
        <div className="chips">
          {selected.length === 0 && <span className="empty">No symptoms selected yet</span>}
          {selected.map((s) => (
            <span key={s} className="chip" onClick={() => removeSymptom(s)}>
              {pretty(s)} <b>×</b>
            </span>
          ))}
        </div>

        <div className="actions">
          <button className="primary" onClick={handlePredict} disabled={loading}>
            {loading ? <span className="spinner" /> : "Predict Disease"}
          </button>
          <button className="ghost" onClick={handleReset}>
            Reset
          </button>
        </div>

        {error && <div className="error">⚠️ {error}</div>}

        {result && (
          <section className="result">
            <p className="result-label">Predicted disease</p>
            <h2>{result.disease}</h2>
            <p className="desc">{result.description}</p>

            <h3>🛡️ Precautions</h3>
            <ul className="precautions">
              {result.precautions.map((p, i) => (
                <li key={i}>
                  <span className="tick">✓</span> {p}
                </li>
              ))}
            </ul>
          </section>
        )}
      </main>

      <footer className="note">
        ⚠️ For learning only. This is not medical advice. Please consult a doctor.
      </footer>
    </div>
  );
}

export default App;
