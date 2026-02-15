import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/* =====================================================
   EVIDENCE SENTENCE HIGHLIGHTING (Aggroso AI Style)
   ===================================================== */

function highlightEvidenceSentence(snippet, answer) {
  if (!answer || !snippet) return snippet;

  // Split snippet into sentences
  const sentences =
    snippet.match(/[^.!?]+[.!?]+/g) || [snippet];

  // Extract meaningful words from answer
  const keywords = answer
    .toLowerCase()
    .replace(/[^\w\s]/g, "")
    .split(/\s+/)
    .filter((w) => w.length > 3);

  let bestSentence = "";
  let bestScore = 0;

  // Find sentence most aligned with answer meaning
  sentences.forEach((sentence) => {
    const lower = sentence.toLowerCase();

    let score = 0;
    keywords.forEach((word) => {
      if (lower.includes(word)) score++;
    });

    if (score > bestScore) {
      bestScore = score;
      bestSentence = sentence;
    }
  });

  // If nothing matched, return original snippet
  if (!bestSentence) return snippet;

  // Highlight entire evidence sentence
  return snippet.replace(
    bestSentence,
    `<mark class="bg-yellow-200 px-1 rounded font-medium">
      ${bestSentence}
     </mark>`
  );
}

/* =====================================================
   CONFIDENCE LABEL (Product UX — no percentages)
   ===================================================== */

function confidenceLabel(score) {
  if (score >= 0.7) {
    return {
      text: "High",
      style:
        "text-green-700 bg-green-50 border-green-200",
    };
  }

  if (score >= 0.4) {
    return {
      text: "Medium",
      style:
        "text-yellow-700 bg-yellow-50 border-yellow-200",
    };
  }

  return {
    text: "Low",
    style:
      "text-red-700 bg-red-50 border-red-200",
  };
}

/* =====================================================
   COMPONENT
   ===================================================== */

export default function ChatMessage({ msg }) {
  const isUser = msg.role === "user";

  return (
    <div
      className={`flex fade-in ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div
        className={`
          max-w-3xl px-6 py-4 rounded-2xl
          shadow-sm transition-all duration-200
          ${
            isUser
              ? "bg-indigo-600 text-white ml-auto"
              : "bg-white border border-slate-200"
          }
        `}
      >
        {/* ================= USER MESSAGE ================= */}
        {isUser ? (
          <div className="whitespace-pre-wrap leading-relaxed">
            {msg.content}
          </div>
        ) : (
          <>
            {/* ================= AI ANSWER ================= */}
            <div className="prose prose-sm max-w-none text-slate-800">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {msg.content}
              </ReactMarkdown>
            </div>

            {/* ================= CONFIDENCE ================= */}
            {msg.confidence !== undefined && (() => {
              const conf = confidenceLabel(msg.confidence);

              return (
                <div className="mt-4 flex items-center gap-2 text-xs font-medium">
                  <span className="text-slate-500">
                    Grounded Answer Confidence:
                  </span>

                  <span
                    title="Confidence reflects how strongly the answer is supported by retrieved document evidence."
                    className={`
                      px-3 py-1 rounded-full border font-semibold
                      ${conf.style}
                    `}
                  >
                    {conf.text}
                  </span>
                </div>
              );
            })()}

            {/* ================= SOURCES ================= */}
            {msg.sources && msg.sources.length > 0 && (
              <div className="mt-5 pt-4 border-t border-slate-200">
                <div className="text-xs font-semibold text-slate-500 mb-3">
                  SOURCES USED
                </div>

                <div className="space-y-3">
                  {msg.sources.map((s, i) => (
                    <div
                      key={i}
                      className="
                        bg-slate-50
                        border border-slate-200
                        rounded-xl
                        p-3
                        hover:shadow-md
                        transition-all
                      "
                    >
                      {/* Document name */}
                      <div className="text-sm font-semibold text-indigo-700">
                        {s.document}
                      </div>

                      {/* Evidence label */}
                      <div className="text-xs text-indigo-500 mt-2 mb-1 font-medium">
                        Evidence used for answer
                      </div>

                      {/* Highlighted snippet */}
                      <div
                        className="
                          text-sm text-slate-700
                          bg-white border rounded-lg
                          p-3 leading-relaxed
                        "
                        dangerouslySetInnerHTML={{
                          __html: highlightEvidenceSentence(
                            s.snippet,
                            msg.content
                          ),
                        }}
                      />
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
