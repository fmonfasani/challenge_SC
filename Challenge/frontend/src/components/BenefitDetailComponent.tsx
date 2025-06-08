import React from "react";
import { Benefit } from "../types/Benefit";

interface BenefitDetailComponentProps {
  benefit: Benefit;
  onClose: () => void;
  isFavorite: boolean;
  onToggleFavorite: (id: number) => void;
}

const BenefitDetailComponent: React.FC<BenefitDetailComponentProps> = ({
  benefit,
  onClose,
  isFavorite,
  onToggleFavorite,
}) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b p-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">{benefit.name}</h2>
          <div className="flex items-center gap-2">
            {/* Botón de favorito */}
            <button
              onClick={() => onToggleFavorite(benefit.id)}
              className="p-2 hover:bg-gray-100 rounded-full"
              title={isFavorite ? "Quitar de favoritos" : "Agregar a favoritos"}
            >
              <svg
                className={`w-6 h-6 ${
                  isFavorite ? "text-red-500 fill-current" : "text-gray-400"
                }`}
                fill={isFavorite ? "currentColor" : "none"}
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                />
              </svg>
            </button>
            {/* Botón de cerrar */}
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-full"
              title="Cerrar"
            >
              ✖
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6">
          <img
            src={benefit.image}
            alt={benefit.name}
            className="w-full h-64 object-cover rounded-lg mb-6"
            loading="lazy"
          />
          <div className="space-y-4">
            <p className="text-gray-700 leading-relaxed">
              {benefit.fullDescription || benefit.description}
            </p>
            {benefit.category && (
              <div className="flex items-center gap-2">
                <span className="font-semibold text-gray-800">Categoría:</span>
                <span className="text-blue-800 bg-blue-100 px-2 py-1 rounded-full text-sm">
                  {benefit.category}
                </span>
              </div>
            )}
            {benefit.validUntil && (
              <div className="flex items-center gap-2">
                <span className="font-semibold text-gray-800">
                  Válido hasta:
                </span>
                <span className="text-gray-700">
                  {new Date(benefit.validUntil).toLocaleDateString("es-ES")}
                </span>
              </div>
            )}
            <div className="flex items-center gap-2">
              <span className="font-semibold text-gray-800">Estado:</span>
              <span
                className={`px-2 py-1 rounded-full text-xs font-medium ${
                  benefit.status === "active"
                    ? "bg-green-100 text-green-800"
                    : "bg-red-100 text-red-800"
                }`}
              >
                {benefit.status === "active" ? "Activo" : "Inactivo"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BenefitDetailComponent;
