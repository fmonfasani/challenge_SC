export interface BeneficioResponse {
  id: number;
  name: string;
  description: string;
  status: string;
  image?: string;
  fullDescription?: string;
  category?: string;
  validUntil?: string;
}

export interface BeneficioListResponse {
  beneficios: BeneficioResponse[];
  total: number;
}

// Configuración de la API
const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000/api";

class ApiService {
  private async makeRequest<T>(endpoint: string): Promise<T> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`API Error for ${endpoint}:`, error);
      throw error;
    }
  }

  // GET /api/beneficios
  async getBeneficios(): Promise<BeneficioListResponse> {
    return this.makeRequest<BeneficioListResponse>("/beneficios");
  }

  // GET /api/beneficios/:id
  async getBeneficioById(id: number): Promise<BeneficioResponse> {
    return this.makeRequest<BeneficioResponse>(`/beneficios/${id}`);
  }

  // Health check para verificar conectividad
  async healthCheck(): Promise<{ status: string }> {
    try {
      const baseUrl = API_BASE_URL.replace("/api", "");
      const response = await fetch(`${baseUrl}/health`);
      if (response.ok) {
        return await response.json();
      }
      return { status: "error" };
    } catch (error) {
      return { status: "error" };
    }
  }
}

export const apiService = new ApiService();
