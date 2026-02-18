import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/* ================= SAFE TEXT ================= */

function normalizeText(value) {
  if (!value) return "";
  if (typeof value !== "string") return String(value);
  return value.trim();
}

/* ================= SAFE HIGHLIGHT =================
   NO innerHTML → prevents XSS completely
=================================================== */

function highlightEvidenceSentence(snippet, answer) {
  snippet = normalizeText(snippet);
  answer = normalizeText(answer);

  if (!snippet) {
    return (
      <span className="text-slate-400 italic">
        No evidence text returned from backend
      </span>
    );
  }

  const sentences =
    snippet.match(/[^.!?]+[.!?]+/g) || [snippet];

  const keywords = answer
    .toLowerCase()
    .replace(/[^\w\s]/g, "")
    .split(/\s+/)
    .filter((w) => w.length > 3);

  let bestSentence = "";
  let bestScore = 0;

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

  if (!bestSentence) return snippet;

  const parts = snippet.split(bestSentence);

  return (
    <>
      {parts[0]}
      <mark className="bg-yellow-200 px-1 rounded font-medium">
        {bestSentence}
      </mark>
      {parts[1]}
    </>
  );
}

/* ================= CONFIDENCE ================= */

function confidenceLabel(score) {
  if (score === "High" || score >= 0.7)
    return {
      text: "High",
      style: "text-green-700 bg-green-50 border-green-200",
    };

  if (score === "Medium" || score >= 0.4)
    return {
      text: "Medium",
      style: "text-yellow-700 bg-yellow-50 border-yellow-200",
    };

  return {
    text: "Low",
    style: "text-red-700 bg-red-50 border-red-200",
  };
}

/* ================= COMPONENT ================= */

export default function ChatMessage({ msg }) {
  const isUser = msg.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-3xl px-6 py-4 rounded-2xl shadow-sm
        ${
          isUser
            ? "bg-indigo-600 text-white"
            : "bg-white border border-slate-200"
        }`}
      >
        {isUser ? (
          <div className="whitespace-pre-wrap">
            {msg.content}
          </div>
        ) : (
          <>
            {/* ANSWER */}
            <div className="prose prose-sm max-w-none text-slate-800">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {msg.content}
              </ReactMarkdown>
            </div>

            {/* CONFIDENCE */}
            {msg.confidence && (() => {
              const conf = confidenceLabel(msg.confidence);

              return (
                <div className="mt-4 flex gap-2 text-xs font-medium">
                  <span className="text-slate-500">
                    Grounded Answer Confidence:
                  </span>

                  <span
                    className={`px-3 py-1 rounded-full border font-semibold ${conf.style}`}
                  >
                    {conf.text}
                  </span>
                </div>
              );
            })()}

            {/* SOURCES */}
            {msg.sources?.length > 0 && (
              <div className="mt-5 pt-4 border-t border-slate-200">
                <div className="text-xs font-semibold text-slate-500 mb-3">
                  SOURCES USED
                </div>

                <div className="space-y-3">
                  {msg.sources.map((s, i) => {
                    const snippet =
                      typeof s.text === "string"
                        ? s.text
                        : typeof s.snippet === "string"
                        ? s.snippet
                        : "";

                    return (
                      <div
                        key={i}
                        className="bg-slate-50 border border-slate-200 rounded-xl p-3"
                      >
                        <div className="text-sm font-semibold text-indigo-700">
                          {s.document}
                        </div>

                        <div className="text-xs text-indigo-500 mt-2 mb-1 font-medium">
                          Evidence used for answer
                        </div>

                        <div className="text-sm text-slate-700 bg-white border rounded-lg p-3 leading-relaxed">
                          {highlightEvidenceSentence(
                            snippet,
                            msg.content
                          )}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
