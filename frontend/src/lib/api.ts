import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  timeout: 150000,
});

api.interceptors.response.use(
  (r) => r,
  (e) => {
    const msg =
      e?.response?.data?.message ||
      e?.response?.data?.detail ||
      e?.message ||
      "Request failed";
    return Promise.reject(new Error(msg));
  }
);
