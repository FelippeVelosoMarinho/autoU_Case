import axios from "axios";

export const api = axios.create({
    baseURL: "http://localhost:8001",
    //baseURL: import.meta.env.API_URL,
  });