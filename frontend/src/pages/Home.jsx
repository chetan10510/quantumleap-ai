import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import ChatWindow from "../components/ChatWindow";
import DocumentSidebar from "../components/DocumentSidebar";
import { getDocuments } from "../services/api";

export default function Home() {
  const navigate = useNavigate();

  // Knowledge status indicator
  const [hasDocuments, setHasDocuments] = useState(false);

  // Check if knowledge base has documents
  const checkKnowledgeStatus = async () => {
    try {
      const res = await getDocuments();
      setHasDocuments((res.documents || []).length > 0);
    } catch {
      setHasDocuments(false);
    }
  };

  useEffect(() => {
    checkKnowledgeStatus();
  }, []);

  return (
    <div className="h-screen flex bg-slate-100">

      {/* ================= SIDEBAR ================= */}
      <div
        className="
          w-72
          bg-gradient-to-b
          from-indigo-900
          to-indigo-800
          text-white
          shadow-xl
        "
      >
        <DocumentSidebar />
      </div>

      {/* ================= MAIN AREA ================= */}
      <div className="flex-1 flex flex-col">

        {/* ================= HEADER ================= */}
        <header
          className="
            h-16
            flex items-center justify-between
            px-8
            backdrop-blur-md
            bg-white/70
            border-b
            sticky top-0
            z-10
          "
        >
          {/* LEFT SIDE */}
          <div>
            <h1 className="text-lg font-semibold text-slate-800">
              Aggroso — Private Knowledge Workspace
            </h1>

            <p className="text-xs text-slate-500">
              AI-Driven Knowledge Intelligence
            </p>
          </div>

          {/* RIGHT SIDE CONTROLS */}
          <div className="flex items-center gap-4">

            {/* KNOWLEDGE STATUS BADGE */}
            <div
              className={`
                px-3 py-1
                text-xs font-medium
                rounded-full
                transition
                ${
                  hasDocuments
                    ? "bg-emerald-100 text-emerald-700"
                    : "bg-slate-200 text-slate-600"
                }
              `}
            >
              {hasDocuments
                ? "Knowledge Active"
                : "No Documents Loaded"}
            </div>

            {/* STATUS PAGE BUTTON */}
            <button
              onClick={() => navigate("/status")}
              className="
                text-sm font-medium
                px-4 py-2
                rounded-lg
                bg-indigo-50
                hover:bg-indigo-100
                text-indigo-700
                transition
                active:scale-95
              "
            >
              System Status
            </button>
          </div>
        </header>

        {/* ================= CHAT AREA ================= */}
        <div className="flex-1 overflow-hidden">
          <ChatWindow />
        </div>

      </div>
    </div>
  );
}
