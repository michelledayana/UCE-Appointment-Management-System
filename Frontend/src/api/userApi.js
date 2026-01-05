import axios from "axios";

const API_URL = "http://localhost:8081";

export const registerUser = async (data) => {
  const response = await axios.post(
    `${API_URL}/users/register`,
    data
  );
  return response.data;
};
