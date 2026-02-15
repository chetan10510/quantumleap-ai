import { useState, useRef, useEffect } from "react";
import ChatInput from "./ChatInput";
import ChatMessage from "./ChatMessage";
import { sendMessage } from "../services/api";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  /* =====================================================
     AUTO SCROLL
  ===================================================== */
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  /* =====================================================
     SAFE CHAT SEND (NORMALIZED API CONTRACT)
  ===================================================== */
  const handleSend = async (text) => {
    if (!text || !text.trim()) return;

    const userMsg = {
      role: "user",
      content: text,
    };

    // show user message instantly
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const data = await sendMessage(text);

      /* ---------- HARD NORMALIZATION LAYER ---------- */

      const safeAnswer =
        typeof data?.answer === "string" &&
        data.answer.trim().length > 0
          ? data.answer
          : "No grounded answer could be generated from the documents.";

      const safeSources = Array.isArray(data?.sources)
        ? data.sources
        : [];

      const safeConfidence =
        typeof data?.confidence === "number"
          ? data.confidence
          : 0.3;

      const aiMsg = {
        role: "assistant",
        content: safeAnswer,
        sources: safeSources,
        confidence: safeConfidence,
      };

      setMessages((prev) => [...prev, aiMsg]);

    } catch (error) {
      console.error("CHAT ERROR:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Sorry, something went wrong while contacting the AI service.",
          sources: [],
          confidence: 0,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  /* =====================================================
     UI
  ===================================================== */
  return (
    <div className="flex flex-col h-full">

      {/* ================= CHAT AREA ================= */}
      <div
        className="
          flex-1 overflow-y-auto
          px-10 py-8
          space-y-6
          bg-gradient-to-b
          from-slate-50
          to-slate-100
        "
      >
        {/* EMPTY STATE */}
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-20">
            <p className="text-lg font-medium">
              Welcome!
            </p>
            <p className="mt-2">
              Upload documents to activate Aggroso AI knowledge reasoning.
            </p>
          </div>
        )}

        {/* CHAT MESSAGES */}
        {messages.map((msg, i) => (
          <ChatMessage key={i} msg={msg} />
        ))}

        {/* THINKING INDICATOR */}
        {loading && (
          <div className="flex items-center gap-2 text-slate-500">
            <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce"></span>
            <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:0.15s]"></span>
            <span className="w-2 h-2 bg-indigo-500 rounded-full animate-bounce [animation-delay:0.3s]"></span>
            <span className="text-sm ml-2">
              Aggroso AI is thinking...
            </span>
          </div>
        )}

        {/* AUTO SCROLL ANCHOR */}
        <div ref={bottomRef} />
      </div>

      {/* ================= INPUT ================= */}
      <ChatInput onSend={handleSend} loading={loading} />
    </div>
  );
}
