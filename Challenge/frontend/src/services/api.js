import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const getBeneficios = async () => {
  const response = await axios.get(`${API_URL}/beneficios`);
  return response.data;
};

export const getBeneficioById = async (id) => {
  const response = await axios.get(`${API_URL}/beneficios/${id}`);
  return response.data;
};
