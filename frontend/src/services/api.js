import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const sendMessage = async (message) => {
  const res = await API.post("/chat/", {
    message: message,
  });

  return res.data;
};

export const getDocuments = async () => {
  const res = await API.get("/documents/");
  return res.data;
};
export const getStatus = async () => {
  const res = await fetch("http://127.0.0.1:8000/status/");
  return res.json();
};


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

export const deleteDocument = async (docId) => {
  const res = await fetch(
    `http://127.0.0.1:8000/documents/${docId}`,
    {
      method: "DELETE",
    }
  );

  if (!res.ok) throw new Error("Delete failed");

  return res.json();
};

