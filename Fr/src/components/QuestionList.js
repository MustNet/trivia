import { useEffect, useState } from "react";
import { api } from "../api";

export default function QuestionList({ categoryId }) {
  const [items, setItems] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [searching, setSearching] = useState(false);

  const load = async (p = 1) => {
    const data = categoryId
      ? await api.getByCategory(categoryId, p)
      : await api.getQuestions(p);
    setItems(data.questions || []);
    setTotal(data.total_questions || 0);
    setPage(p);
  };

  useEffect(() => { load(1); /* eslint-disable-next-line */ }, [categoryId]);

  const onDelete = async (id) => {
    await api.deleteQuestion(id);
    // reload current page; if page becomes empty, go back one page
    if (items.length === 1 && page > 1) await load(page - 1);
    else await load(page);
  };

  const onSearch = async (term) => {
    if (!term) { setSearching(false); return load(1); }
    const data = await api.searchQuestions(term);
    setSearching(true);
    setItems(data.questions || []);
    setTotal(data.total_questions || 0);
    setPage(1);
  };

  const pageCount = Math.ceil(total / 10) || 1;

  return (
    <div className="card">
      <h3>Questions {categoryId ? <span className="tag">Category {categoryId}</span> : null}</h3>

      {/* inline search */}
      <div style={{ margin: "8px 0" }}>
        <input className="input" placeholder="Search…" onKeyDown={(e) => {
          if (e.key === "Enter") onSearch(e.target.value.trim());
        }} />
      </div>

      {items.length === 0 ? <p>No questions found.</p> : (
        <ul className="grid">
          {items.map(q => (
            <li key={q.id} className="card">
              <strong>{q.question}</strong>
              <div>Answer: {q.answer}</div>
              <div>Cat: {q.category} • Diff: {q.difficulty}</div>
              <button className="btn danger" onClick={() => onDelete(q.id)}>Delete</button>
            </li>
          ))}
        </ul>
      )}

      {!searching && (
        <div className="pagination">
          <button className="btn" disabled={page<=1} onClick={() => load(page-1)}>Prev</button>
          <div>Page {page} / {pageCount}</div>
          <button className="btn" disabled={page>=pageCount} onClick={() => load(page+1)}>Next</button>
        </div>
      )}
    </div>
  );
}
