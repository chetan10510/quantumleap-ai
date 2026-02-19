import axios from "axios";

const API = axios.create({
  baseURL: "https://quantamleap-ai-backend-production.up.railway.app",
});

/* ---------- CHAT ---------- */
export const sendMessage = async (message) => {
  const res = await API.post("/chat/", { message });
  return res.data;
};

/* ---------- DOCUMENTS ---------- */
export const getDocuments = async () => {
  const res = await API.get("/documents/");
  return res.data;
};

/* ---------- STATUS ---------- */
export const getStatus = async () => {
  const res = await API.get("/status/");
  return res.data;
};

/* ---------- UPLOAD ---------- */
export const uploadFiles = async (files) => {
  const formData = new FormData();

  for (let file of files) {
    formData.append("files", file);
  }

  const res = await API.post("/upload/", formData);

  return res.data;
};

/* ---------- DELETE ---------- */
export const deleteDocument = async (docId) => {
  if (!docId) throw new Error("Invalid document id");

  const res = await API.delete(`/documents/${docId}`);
  return res.data;
};
