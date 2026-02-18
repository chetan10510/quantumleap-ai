import { useNavigate } from "react-router-dom";

export default function Welcome() {
  const navigate = useNavigate();

  return (
    <div className="
      min-h-screen
      flex flex-col
      items-center
      justify-center
      px-6
      bg-gradient-to-br
      from-indigo-50
      via-white
      to-slate-100
    ">
      {/* BRAND */}
      <div className="text-center max-w-3xl">

        <h1 className="
          text-4xl font-semibold tracking-tight
          text-slate-900
        ">
          Quantumleap Private Knowledge Workspace
        </h1>

        <p className="mt-4 text-lg text-slate-600">
          Upload documents, ask questions, and receive grounded
          AI answers with transparent source references.
        </p>
      </div>

      {/* STEPS */}
      <div className="
        mt-12
        grid md:grid-cols-3
        gap-6
        max-w-5xl
        w-full
      ">

        {/* Step 1 */}
        <div className="
          bg-white
          rounded-2xl
          p-6
          shadow-sm
          border
          hover:shadow-md
          transition
        ">
          <h3 className="font-semibold text-lg">
            1. Upload Documents
          </h3>
          <p className="mt-2 text-sm text-slate-600">
            Add PDFs, Word files, Excel sheets or text files
            to create your private knowledge base.
          </p>
        </div>

        {/* Step 2 */}
        <div className="
          bg-white rounded-2xl p-6 shadow-sm border
          hover:shadow-md transition
        ">
          <h3 className="font-semibold text-lg">
            2. Ask Questions
          </h3>
          <p className="mt-2 text-sm text-slate-600">
            Interact through a chat interface powered by
            semantic search and AI reasoning.
          </p>
        </div>

        {/* Step 3 */}
        <div className="
          bg-white rounded-2xl p-6 shadow-sm border
          hover:shadow-md transition
        ">
          <h3 className="font-semibold text-lg">
            3. View Sources
          </h3>
          <p className="mt-2 text-sm text-slate-600">
            Every answer shows supporting document
            excerpts for transparency and trust.
          </p>
        </div>

      </div>

      {/* CTA */}
      <button
        onClick={() => navigate("/home")}
        className="
          mt-12
          px-8 py-4
          rounded-xl
          text-white font-medium
          bg-indigo-600
          hover:bg-indigo-700
          shadow-lg
          hover:shadow-xl
          transition-all
          active:scale-95
        "
      >
        Open Workspace
      </button>

      {/* FOOTER */}
      <p className="mt-10 text-xs text-slate-400">
        QuantumLeap — AI Knowledge Automation LLM-powered Knowledge Agent
      </p>
    </div>
  );
}
