import { useEffect, useState } from "react";
import { getStatus } from "../services/api";

export default function Status() {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const res = await getStatus();
        setStatus(res);
      } catch (err) {
        setStatus({ error: "Unable to reach backend" });
      } finally {
        setLoading(false);
      }
    };

    fetchStatus();
  }, []);

  const Badge = ({ ok }) => (
    <span
      className={`px-3 py-1 rounded-full text-xs font-medium ${
        ok
          ? "bg-green-100 text-green-700"
          : "bg-red-100 text-red-700"
      }`}
    >
      {ok ? "Healthy" : "Unavailable"}
    </span>
  );

  return (
    <div className="p-10 max-w-3xl mx-auto">

      <h1 className="text-2xl font-semibold mb-6">
        System Status
      </h1>

      {loading && <p>Checking system health...</p>}

      {status && (
        <div className="space-y-4">

          <div className="bg-white border rounded-xl p-5 flex justify-between">
            <span>Backend API</span>
            <Badge ok={status.backend === "ok"} />
          </div>

          <div className="bg-white border rounded-xl p-5 flex justify-between">
            <span>Database</span>
            <Badge ok={status.database === "ok"} />
          </div>

          <div className="bg-white border rounded-xl p-5 flex justify-between">
            <span>LLM Connection</span>
            <Badge ok={status.llm === "ok"} />
          </div>

        </div>
      )}
    </div>
  );
}
