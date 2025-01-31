import axios from "axios";

export const api = axios.create({
    // baseURL: "http://localhost:8001",
    baseURL: "https://apiautoucase-production.up.railway.app/,"
  });