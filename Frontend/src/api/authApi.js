import axios from "axios";

const API_URL = "http://localhost:8081";

export const registerUser = (data) =>
  axios.post(`${API_URL}/register`, data);

export const loginUser = (data) =>
  axios.post(`${API_URL}/login`, data);
