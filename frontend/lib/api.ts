const API_BASE = "http://localhost:8000";

export async function getTransactions() {
  const res = await fetch(`${API_BASE}/transactions`, { cache: "no-store" });
  return res.json();
}

export async function getSummary() {
  const res = await fetch(`${API_BASE}/summary`, { cache: "no-store" });
  return res.json();
}

export async function getCategoryBreakdown() {
  const res = await fetch(`${API_BASE}/category-breakdown`, { cache: "no-store" });
  return res.json();
}

export async function getInsights() {
  const res = await fetch(`${API_BASE}/insights`, { cache: "no-store" });
  return res.json();
}

export async function uploadTransactions(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/upload-transactions`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Upload failed");
  }

  return res.json();
}
export async function getLatestUpload() {
    const res = await fetch(`${API_BASE}/latest-upload`, { cache: "no-store" });
    return res.json();
  }