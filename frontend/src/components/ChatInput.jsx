import { useState } from "react";

export default function ChatInput({ onSend, loading }) {
  const [text, setText] = useState("");
  const [error, setError] = useState("");

  const handleSend = () => {
    const cleaned = text.trim();

    if (!cleaned) {
      setError("Please enter a question.");
      return;
    }

    if (loading) return;

    setError("");
    onSend(cleaned);
    setText("");
  };

  return (
    <div className="
      border-t
      bg-white
      px-8 py-5
      flex flex-col gap-2
      shadow-[0_-4px_20px_rgba(0,0,0,0.05)]
    ">

      <div className="flex gap-4 items-end">

        {/* TEXT AREA */}
        <textarea
          className={`
            flex-1
            rounded-xl
            border
            p-4
            resize-none
            transition-all duration-200
            focus:outline-none
            focus:ring-2 focus:ring-indigo-500
            ${
              loading
                ? "bg-slate-100 cursor-not-allowed border-slate-200"
                : "bg-slate-50 border-slate-300 hover:border-slate-400"
            }
          `}
          placeholder="Ask QuantumLeap AI about your documents..."
          rows={2}
          value={text}
          disabled={loading}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
        />

        {/* SEND BUTTON */}
        <button
          onClick={handleSend}
          disabled={loading}
          className={`
            px-7 py-3
            rounded-xl
            font-medium
            text-white
            transition-all duration-150
            ${
              loading
                ? "bg-slate-400 cursor-not-allowed"
                : "bg-indigo-600 hover:bg-indigo-700 active:scale-95 shadow-lg hover:shadow-xl"
            }
          `}
        >
          {loading ? "Processing..." : "Send"}
        </button>
      </div>

      {/* ERROR MESSAGE */}
      {error && (
        <p className="text-sm text-red-500">
          {error}
        </p>
      )}
    </div>
  );
}
