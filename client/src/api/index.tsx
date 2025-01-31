import axios from "axios";

export const api = axios.create({
    // baseURL: "http://localhost:8001",
    baseURL: "https://fastapi-production-e543.up.railway.app,"
  });