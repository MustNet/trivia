const BASE = process.env.REACT_APP_API_BASE || "";

async function req(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const text = await res.text();
  const data = text ? JSON.parse(text) : {};
  if (!res.ok) throw new Error(data.message || res.statusText);
  return data;
}

export const api = {
  getCategories: () => req("/categories"),
  getQuestions: (page = 1) => req(`/questions?page=${page}`),
  searchQuestions: (term) =>
    req("/questions/search", { method: "POST", body: JSON.stringify({ searchTerm: term }) }),
  createQuestion: (q) =>
    req("/questions", { method: "POST", body: JSON.stringify(q) }),
  deleteQuestion: (id) => req(`/questions/${id}`, { method: "DELETE" }),
  getByCategory: (id, page = 1) =>
    req(`/categories/${id}/questions${page ? `?page=${page}` : ""}`),
};
