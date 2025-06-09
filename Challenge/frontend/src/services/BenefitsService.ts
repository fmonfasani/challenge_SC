import { Benefit } from "../types/Benefit";
import { mockBenefits } from "../mock/mockBenefits";

export interface BenefitsResult {
  benefits: Benefit[];
  total: number;
  source: "api" | "mock";
}

export class BenefitsService {
  private static readonly API_BASE_URL =
    import.meta.env.VITE_API_URL || "http://localhost:8000/api";

  static async getAllBenefits(): Promise<BenefitsResult> {
    console.log("🔍 BenefitsService: Iniciando getAllBenefits()");
    console.log("🔍 API_BASE_URL:", this.API_BASE_URL);
    console.log("🔍 VITE_API_URL env:", import.meta.env.VITE_API_URL);

    try {
      console.log("🔍 Intentando health check...");
      const healthUrl = `${this.API_BASE_URL.replace("/api", "")}/health`;
      console.log("🔍 Health URL:", healthUrl);

      const healthResponse = await fetch(healthUrl, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      console.log("🔍 Health response status:", healthResponse.status);

      if (!healthResponse.ok) {
        throw new Error(`Health check failed: ${healthResponse.status}`);
      }

      const healthData = await healthResponse.json();
      console.log("🔍 Health check successful:", healthData);

      console.log("🔍 Intentando obtener beneficios...");
      const beneficiosUrl = `${this.API_BASE_URL}/beneficios`;
      console.log("🔍 Beneficios URL:", beneficiosUrl);

      const response = await fetch(beneficiosUrl, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      console.log("🔍 Beneficios response status:", response.status);
      console.log(
        "🔍 Beneficios response headers:",
        Object.fromEntries(response.headers.entries())
      );

      if (!response.ok) {
        throw new Error(
          `API request failed: ${response.status} ${response.statusText}`
        );
      }

      const data = await response.json();
      console.log("🔍 API Response data:", data);

      if (!data || typeof data !== "object") {
        throw new Error("Invalid response format: not an object");
      }

      let benefits: Benefit[];
      let total: number;

      if (Array.isArray(data)) {
        benefits = data.map((item: any) => this.adaptBenefitData(item));
        total = benefits.length;
      } else if (data.beneficios && Array.isArray(data.beneficios)) {
        benefits = data.beneficios.map((item: any) =>
          this.adaptBenefitData(item)
        );
        total = data.total || benefits.length;
      } else {
        throw new Error("Invalid response format: no beneficios array found");
      }

      console.log("✅ Datos obtenidos del backend exitosamente");
      console.log("✅ Beneficios procesados:", benefits.length);

      return {
        benefits,
        total,
        source: "api",
      };
    } catch (error) {
      console.warn("❌ Error conectando con el backend:", error);
      console.warn("🔄 Usando datos mock como fallback");
      return this.getMockBenefits();
    }
  }

  private static adaptBenefitData(item: any): Benefit {
    return {
      id: item.id,
      name: item.name || item.nombre,
      description: item.description || item.descripcion,
      image: item.image || item.imagen || "https://via.placeholder.com/400x300",
      status:
        item.status === "active" || item.estado === "activo"
          ? "active"
          : "inactive",
      fullDescription: item.fullDescription || item.descripcion_completa,
      category: item.category || item.categoria,
      validUntil: item.validUntil || item.fecha_vencimiento,
    };
  }

  static async getBenefitById(id: number): Promise<Benefit | null> {
    console.log("🔍 BenefitsService: Obteniendo beneficio por ID:", id);

    try {
      const url = `${this.API_BASE_URL}/beneficios/${id}`;
      console.log("🔍 Benefit by ID URL:", url);

      const response = await fetch(url);
      console.log("🔍 Benefit by ID response status:", response.status);

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`);
      }

      const data = await response.json();
      console.log("🔍 Benefit by ID data:", data);

      return this.adaptBenefitData(data);
    } catch (error) {
      console.warn("❌ Error obteniendo beneficio por ID:", error);
      console.warn("🔄 Usando mock como fallback");
      return mockBenefits.find((benefit) => benefit.id === id) || null;
    }
  }

  private static getMockBenefits(): BenefitsResult {
    console.log("📦 Usando datos mock, total:", mockBenefits.length);
    return {
      benefits: mockBenefits,
      total: mockBenefits.length,
      source: "mock",
    };
  }
}
