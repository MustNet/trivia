import { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [q, setQ] = useState("");
  return (
    <div className="card">
      <form onSubmit={(e) => { e.preventDefault(); onSearch(q.trim()); }}>
        <input className="input" placeholder="Search questions…" value={q} onChange={e => setQ(e.target.value)} />
      </form>
    </div>
  );
}
