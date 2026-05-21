"use client";

import { useState } from "react";
import { uploadTransactions } from "../lib/api";

export default function UploadForm({ onUpload }: { onUpload: () => void }) {
  const [file, setFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadedFileName, setUploadedFileName] = useState("");
  const [downloadUrl, setDownloadUrl] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    try {
      setLoading(true);
      const res = await uploadTransactions(file);
      setMessage(res.message);
      setUploadedFileName(res.filename);
      setDownloadUrl(res.download_url);
      onUpload();
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Upload failed";
      setMessage(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="panel">
      <h2>Upload Transactions</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
        />
        <button type="submit" disabled={loading || !file}>
          {loading ? "Uploading..." : "Upload CSV"}
        </button>
      </form>

      {message && <p>{message}</p>}

      {uploadedFileName && (
        <div style={{ marginTop: "12px" }}>
          <p>
            Uploaded file: <strong>{uploadedFileName}</strong>
          </p>
          <a href={downloadUrl} download>
            Download uploaded file
          </a>
        </div>
      )}

      <p style={{ opacity: 0.8 }}>
        CSV columns required: <strong>date</strong>, <strong>description</strong>, <strong>amount</strong>
      </p>
    </div>
  );
}