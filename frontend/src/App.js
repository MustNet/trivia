import React, { useEffect, useState } from "react";
import { api } from "./api";

const Box = ({ children, style }) => (
  <div style={{ background: "#fff", border: "1px solid #e5e7eb", borderRadius: 12, padding: 16, marginBottom: 16, ...style }}>
    {children}
  </div>
);

export default function App() {
  const [cats, setCats] = useState({});
  const [catId, setCatId] = useState(null);
  const [page, setPage] = useState(1);
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [q, setQ] = useState({ question: "", answer: "", category: 1, difficulty: 1 });
  const [term, setTerm] = useState("");

  const load = async (p = 1, c = catId) => {
    const d = c ? await api.getByCategory(c, p) : await api.getQuestions(p);
    setItems(d.questions || []);
    setTotal(d.total_questions || 0);
    setPage(p);
  };

  useEffect(() => { api.getCategories().then(d => setCats(d.categories || {})); }, []);
  useEffect(() => { load(1); /* reload when category changes */ }, [catId]);

  const pageCount = Math.max(1, Math.ceil((total || 0) / 10));

  return (
    <div style={{ fontFamily: "system-ui, Arial", padding: 24, maxWidth: 1000, margin: "0 auto" }}>
      <h2>Trivia App</h2>

      {/* Categories */}
      <Box>
        <strong>Categories:</strong>{" "}
        <button onClick={() => setCatId(null)} style={{ marginRight: 8, padding: "4px 8px" }}>
          All
        </button>
        {Object.entries(cats).map(([id, name]) => (
          <button key={id} onClick={() => setCatId(Number(id))} style={{ marginRight: 8, padding: "4px 8px" }}>
            {name}
          </button>
        ))}
      </Box>

      {/* Search */}
      <Box>
        <form onSubmit={async e => { e.preventDefault();
          if (!term.trim()) return load(1);
          const d = await api.searchQuestions(term.trim());
          setItems(d.questions || []); setTotal(d.total_questions || 0); setPage(1);
        }}>
          <input
            value={term}
            onChange={e => setTerm(e.target.value)}
            placeholder="Search questions…"
            style={{ padding: 8, border: "1px solid #e5e7eb", borderRadius: 8, width: 300, marginRight: 8 }}
          />
          <button type="submit">Search</button>
        </form>
      </Box>

      {/* Add Question */}
      <Box>
        <form onSubmit={async e => {
          e.preventDefault();
          await api.createQuestion({
            question: q.question.trim(),
            answer: q.answer.trim(),
            category: Number(q.category),
            difficulty: Number(q.difficulty),
          });
          setQ({ question: "", answer: "", category: 1, difficulty: 1 });
          setTerm(""); await load(page);
        }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
            <input placeholder="Question" value={q.question} onChange={e => setQ({ ...q, question: e.target.value })} />
            <input placeholder="Answer" value={q.answer} onChange={e => setQ({ ...q, answer: e.target.value })} />
            <input placeholder="Category ID" type="number" value={q.category} onChange={e => setQ({ ...q, category: e.target.value })} />
            <input placeholder="Difficulty 1-5" type="number" min="1" max="5" value={q.difficulty} onChange={e => setQ({ ...q, difficulty: e.target.value })} />
          </div>
          <button style={{ marginTop: 8 }}>Create</button>
        </form>
      </Box>

      {/* Questions list */}
      <Box>
        <h3>Questions {catId ? `(Category ${catId})` : ""}</h3>
        {items.length === 0 ? <p>No questions.</p> : (
          <ul style={{ listStyle: "none", paddingLeft: 0 }}>
            {items.map(x => (
              <li key={x.id} style={{ borderBottom: "1px solid #eee", padding: "8px 0" }}>
                <div><strong>{x.question}</strong></div>
                <div>Answer: {x.answer} • Cat: {x.category} • Diff: {x.difficulty}</div>
                <button
                  onClick={async () => { await api.deleteQuestion(x.id); await load(items.length === 1 && page > 1 ? page - 1 : page); }}
                  style={{ background: "#ef4444", color: "#fff", border: 0, padding: "6px 10px", borderRadius: 6, marginTop: 6 }}
                >Delete</button>
              </li>
            ))}
          </ul>
        )}
        <div style={{ marginTop: 8 }}>
          <button disabled={page <= 1} onClick={() => load(page - 1)} style={{ marginRight: 8 }}>Prev</button>
          Page {page} / {pageCount}
          <button disabled={page >= pageCount} onClick={() => load(page + 1)} style={{ marginLeft: 8 }}>Next</button>
        </div>
      </Box>
    </div>
  );
}
