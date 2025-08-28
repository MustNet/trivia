import { useState } from "react";
import { api } from "../api";

export default function AddQuestionForm({ onCreated }) {
  const [form, setForm] = useState({ question: "", answer: "", category: 1, difficulty: 1 });
  const [busy, setBusy] = useState(false);
  const onChange = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    try {
      await api.createQuestion({
        question: form.question.trim(),
        answer: form.answer.trim(),
        category: Number(form.category),
        difficulty: Number(form.difficulty),
      });
      setForm({ question: "", answer: "", category: 1, difficulty: 1 });
      onCreated?.();
    } finally { setBusy(false); }
  };

  return (
    <div className="card">
      <h3>Add Question</h3>
      <form onSubmit={submit} className="grid">
        <input className="input" placeholder="Question" value={form.question} onChange={onChange("question")} required />
        <input className="input" placeholder="Answer" value={form.answer} onChange={onChange("answer")} required />
        <input className="input" type="number" min="1" placeholder="Category ID" value={form.category} onChange={onChange("category")} required />
        <input className="input" type="number" min="1" max="5" placeholder="Difficulty (1-5)" value={form.difficulty} onChange={onChange("difficulty")} required />
        <button className="btn primary" disabled={busy}>Create</button>
      </form>
    </div>
  );
}
