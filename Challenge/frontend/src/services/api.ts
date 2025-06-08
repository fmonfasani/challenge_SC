import axios from 'axios';

// Definimos el tipo de Beneficio
export interface Beneficio {
  id: number;
  nombre: string;
  descripcion: string;
  estado: string;
  imagen: string;
}

// Creamos una instancia de axios con la baseURL desde el .env
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
});

// GET /beneficios
export const getBeneficios = async (): Promise<Beneficio[]> => {
  const response = await apiClient.get<Beneficio[]>('/beneficios');
  return response.data;
};

// GET /beneficios/:id
export const getBeneficioById = async (id: number): Promise<Beneficio> => {
  const response = await apiClient.get<Beneficio>(`/beneficios/${id}`);
  return response.data;
};

