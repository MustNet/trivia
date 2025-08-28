import { useEffect, useState } from "react";
import { api } from "../api";

export default function Quiz({ categoryId }) {
  const [prev, setPrev] = useState([]);
  const [q, setQ] = useState(null);
  const [showA, setShowA] = useState(false);

  const load = async () => {
    const data = await api.playQuiz(
      categoryId ? { id: categoryId } : { id: 0 },
      prev
    );
    setQ(data.question);
    setShowA(false);
  };

  useEffect(() => { setPrev([]); setQ(null); /* reset when category changes */ }, [categoryId]);

  useEffect(() => { load(); /* eslint-disable-next-line */ }, [prev, categoryId]);

  if (!q) return <div className="card"><h3>Quiz</h3><p>No more questions.</p></div>;

  return (
    <div className="card">
      <h3>Quiz</h3>
      <p><strong>{q.question}</strong></p>
      {showA ? <p>Answer: {q.answer}</p> : <button className="btn" onClick={() => setShowA(true)}>Show answer</button>}
      <div style={{ marginTop: 8 }}>
        <button className="btn primary" onClick={() => setPrev([...prev, q.id])}>Next</button>
      </div>
    </div>
  );
}
