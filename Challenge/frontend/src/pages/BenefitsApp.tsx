import React, { useState, useEffect, useMemo, lazy, Suspense } from "react";
import { Benefit } from "../types/Benefit";
import { FavoritesService } from "../services/FavoritesService";
import { BenefitsService } from "../services/BenefitsService";
import BenefitCard from "../components/BenefitCard";

const BenefitDetailComponent = lazy(
  () => import("../components/BenefitDetailComponent")
);

const BenefitsApp: React.FC = () => {
  const [benefits, setBenefits] = useState<Benefit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dataSource, setDataSource] = useState<"api" | "mock">("mock");
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState<
    "all" | "active" | "inactive"
  >("all");
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedBenefit, setSelectedBenefit] = useState<Benefit | null>(null);
  const [favorites, setFavorites] = useState<number[]>([]);

  const itemsPerPage = 6;

  useEffect(() => {
    const loadBenefits = async () => {
      setLoading(true);
      setError(null);

      try {
        const result = await BenefitsService.getAllBenefits();
        setBenefits(result.benefits);
        setDataSource(result.source);
        setFavorites(FavoritesService.getFavorites());

        console.log(
          `✅ Cargados ${result.total} beneficios desde ${result.source}`
        );
      } catch (err) {
        console.error("Error cargando beneficios:", err);
        setError("Error cargando beneficios");
      } finally {
        setLoading(false);
      }
    };

    loadBenefits();
  }, []);

  const filteredBenefits = useMemo(() => {
    return benefits.filter((benefit) => {
      const matchesSearch = benefit.name
        .toLowerCase()
        .includes(searchTerm.toLowerCase());
      const matchesStatus =
        statusFilter === "all" || benefit.status === statusFilter;
      return matchesSearch && matchesStatus;
    });
  }, [benefits, searchTerm, statusFilter]);

  const totalPages = Math.ceil(filteredBenefits.length / itemsPerPage);
  const paginatedBenefits = filteredBenefits.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handleToggleFavorite = (id: number) => {
    if (favorites.includes(id)) {
      FavoritesService.removeFavorite(id);
      setFavorites((prev) => prev.filter((fav) => fav !== id));
    } else {
      FavoritesService.addFavorite(id);
      setFavorites((prev) => [...prev, id]);
    }
  };

  const handleRefresh = async () => {
    const result = await BenefitsService.getAllBenefits();
    setBenefits(result.benefits);
    setDataSource(result.source);
  };

  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, statusFilter]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando beneficios...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button
            onClick={handleRefresh}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto p-6">
          <div className="flex justify-between items-center">
            <h1 className="text-4xl font-bold text-gray-900">
              Beneficios Sport
            </h1>
            <div className="flex items-center gap-4">
              {/* Indicador de fuente de datos */}
              <span
                className={`px-3 py-1 rounded-full text-sm font-medium ${
                  dataSource === "api"
                    ? "bg-green-100 text-green-800"
                    : "bg-yellow-100 text-yellow-800"
                }`}
              >
                {dataSource === "api" ? "🟢 API Backend" : "🟡 Datos Mock"}
              </span>
              <button
                onClick={handleRefresh}
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
                title="Actualizar datos"
              >
                🔄 Actualizar
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        {/* Filtros */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Buscar beneficios..."
              className="border border-gray-300 rounded-lg px-4 py-2 flex-1 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
            <select
              value={statusFilter}
              onChange={(e) =>
                setStatusFilter(e.target.value as "all" | "active" | "inactive")
              }
              className="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="all">Todos los estados</option>
              <option value="active">Activos</option>
              <option value="inactive">Inactivos</option>
            </select>
          </div>

          {/* Información de resultados */}
          <div className="mt-4 text-sm text-gray-600">
            Mostrando {paginatedBenefits.length} de {filteredBenefits.length}{" "}
            beneficios
            {searchTerm && ` para "${searchTerm}"`}
          </div>
        </div>

        {/* Grid de beneficios */}
        {paginatedBenefits.length > 0 ? (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {paginatedBenefits.map((benefit) => (
                <BenefitCard
                  key={benefit.id}
                  benefit={benefit}
                  onSelect={setSelectedBenefit}
                  isFavorite={favorites.includes(benefit.id)}
                  onToggleFavorite={handleToggleFavorite}
                />
              ))}
            </div>

            {/* Paginación */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center space-x-2 mt-8">
                <button
                  onClick={() =>
                    setCurrentPage((prev) => Math.max(prev - 1, 1))
                  }
                  disabled={currentPage === 1}
                  className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                >
                  Anterior
                </button>

                {/* Números de página */}
                <div className="flex space-x-1">
                  {Array.from({ length: Math.min(totalPages, 5) }, (_, i) => {
                    let pageNumber;
                    if (totalPages <= 5) {
                      pageNumber = i + 1;
                    } else if (currentPage <= 3) {
                      pageNumber = i + 1;
                    } else if (currentPage >= totalPages - 2) {
                      pageNumber = totalPages - 4 + i;
                    } else {
                      pageNumber = currentPage - 2 + i;
                    }

                    return (
                      <button
                        key={pageNumber}
                        onClick={() => setCurrentPage(pageNumber)}
                        className={`px-3 py-2 border rounded-lg transition-colors ${
                          currentPage === pageNumber
                            ? "bg-blue-600 text-white border-blue-600"
                            : "border-gray-300 hover:bg-gray-50"
                        }`}
                      >
                        {pageNumber}
                      </button>
                    );
                  })}
                </div>

                <button
                  onClick={() =>
                    setCurrentPage((prev) => Math.min(prev + 1, totalPages))
                  }
                  disabled={currentPage === totalPages}
                  className="px-4 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50 transition-colors"
                >
                  Siguiente
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">
              No se encontraron beneficios
            </p>
            {searchTerm && (
              <button
                onClick={() => setSearchTerm("")}
                className="mt-4 text-blue-600 hover:text-blue-700 underline"
              >
                Limpiar búsqueda
              </button>
            )}
          </div>
        )}

        {/* Modal de detalle */}
        {selectedBenefit && (
          <Suspense
            fallback={
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                <div className="bg-white rounded-lg p-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                  <p className="mt-4 text-gray-600">Cargando detalle...</p>
                </div>
              </div>
            }
          >
            <BenefitDetailComponent
              benefit={selectedBenefit}
              onClose={() => setSelectedBenefit(null)}
              isFavorite={favorites.includes(selectedBenefit.id)}
              onToggleFavorite={handleToggleFavorite}
            />
          </Suspense>
        )}
      </main>
    </div>
  );
};

export default BenefitsApp;
