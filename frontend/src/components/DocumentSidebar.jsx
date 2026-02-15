import { useEffect, useState } from "react";
import {
  getDocuments,
  uploadFiles,
  deleteDocument,
} from "../services/api";

export default function DocumentSidebar() {

  const [docs, setDocs] = useState([]);
  const [uploading, setUploading] = useState(false);

  // ---------- LOAD DOCUMENTS ----------
  const loadDocs = async () => {
  try {
    const res = await getDocuments();

    const docsArray = Array.isArray(res?.documents)
      ? res.documents
      : [];

    setDocs(docsArray);
  } catch (err) {
    console.error("Failed loading documents", err);
    setDocs([]);
    }
  };

  // ---------- UPLOAD ----------
  const handleUpload = async (e) => {
    const files = e.target.files;
    if (!files.length) return;

    try {
      setUploading(true);

      await uploadFiles(files);

      await loadDocs(); // refresh instantly
      e.target.value = "";
    } catch (err) {
      console.error(err);
    } finally {
      setUploading(false);
    }
  };

  // ---------- DELETE ----------
  const handleDelete = async (docId) => {
    try {
      await deleteDocument(docId);
      await loadDocs();
    } catch (err) {
      console.error("Delete failed", err);
    }
  };

  return (
    <div className="h-full flex flex-col p-5 gap-6">

      {/* HEADER */}
      <div>
        <h2 className="text-xl font-semibold">
          Aggroso
        </h2>
        <p className="text-xs text-indigo-200">
          Knowledge Workspace
        </p>
      </div>

      {/* UPLOAD BUTTON */}
      <label className="cursor-pointer">
        <input
          type="file"
          multiple
          className="hidden"
          onChange={handleUpload}
        />

        <div className="
          bg-white text-indigo-900
          font-medium text-center
          rounded-xl py-3
          shadow-md
          hover:bg-indigo-100
          transition
        ">
          {uploading ? "Uploading..." : "Upload Documents"}
        </div>
      </label>

      {/* DOCUMENT LIST */}
      <div className="flex-1 overflow-y-auto space-y-2">

        {docs.length === 0 ? (
          <p className="text-sm text-indigo-200">
            No documents uploaded
          </p>
        ) : (
          docs.map((doc) => (
            <div
              key={doc.doc_id}
              className="
                bg-indigo-800
                rounded-lg
                px-3 py-2
                flex justify-between items-center
                text-sm
                group
              "
            >
              {/* DOCUMENT NAME (THIS IS WHERE YOU ADD text-white) */}
              <span className="truncate text-white">
                {doc.filename}
              </span>

              {/* DELETE BUTTON (REPLACED CLASS HERE) */}
              <button
                onClick={() => handleDelete(doc.doc_id)}
                className="
                  text-red-300
                  opacity-0
                  group-hover:opacity-100
                  hover:scale-110
                  hover:text-red-500
                  transition-all duration-150
                "
              >
                ✕
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
