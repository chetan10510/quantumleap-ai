import axios from "axios";

/*
  Backend URL
*/
const API = axios.create({
  baseURL: "https://aggroso-backend.onrender.com",
});

/*
  Create persistent device user id
  Each browser = one workspace
*/
const getUserId = () => {
  let id = localStorage.getItem("user_id");

  if (!id) {
    id = crypto.randomUUID();
    localStorage.setItem("user_id", id);
  }

  return id;
};

/*
  Automatically attach user id to every request
*/
API.interceptors.request.use((config) => {
  config.headers["X-User-ID"] = getUserId();
  return config;
});

/* ---------------- CHAT ---------------- */
export const sendMessage = async (message) => {
  const res = await API.post("/chat/", {
    message,
  });
  return res.data;
};

/* ---------------- DOCUMENTS ---------------- */
export const getDocuments = async () => {
  const res = await API.get("/documents/");
  return res.data;
};

/* ---------------- STATUS ---------------- */
export const getStatus = async () => {
  const res = await API.get("/status/");
  return res.data;
};

/* ---------------- UPLOAD ---------------- */
export const uploadFiles = async (files) => {
  const formData = new FormData();

  for (let file of files) {
    formData.append("files", file);
  }

  const res = await API.post("/upload/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return res.data;
};

/* ---------------- DELETE ---------------- */
export const deleteDocument = async (docId) => {
  const res = await API.delete(`/documents/${docId}`);
  return res.data;
};
