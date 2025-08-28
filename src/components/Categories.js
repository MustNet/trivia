import { useEffect, useState } from "react";
import { api } from "../api";

export default function Categories({ current, onSelect }) {
  const [cats, setCats] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getCategories().then(d => { setCats(d.categories || {}); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="card">Loading categories…</div>;

  return (
    <div className="card">
      <h3>Categories</h3>
      <div className="grid">
        {Object.entries(cats).map(([id, name]) => (
          <button
            key={id}
            className={`btn ${current === Number(id) ? "primary" : ""}`}
            onClick={() => onSelect(Number(id))}
          >
            {name}
          </button>
        ))}
        <button className={`btn ${current ? "" : "primary"}`} onClick={() => onSelect(null)}>
          All
        </button>
      </div>
    </div>
  );
}
