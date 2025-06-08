import React from 'react';
import { Benefit } from '../types/Benefit';

interface BenefitDetailComponentProps {
  benefit: Benefit;
  onClose: () => void;
  isFavorite: boolean;
  onToggleFavorite: (id: number) => void;
}

const BenefitDetailComponent: React.FC<BenefitDetailComponentProps> = ({ benefit, onClose, isFavorite, onToggleFavorite }) => {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b p-4 flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">{benefit.name}</h2>
          <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
            ✖
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          <img src={benefit.image} alt={benefit.name} className="w-full h-64 object-cover rounded-lg mb-6" loading="lazy" />
          <div className="space-y-4">
            <p className="text-gray-700 leading-relaxed">{benefit.fullDescription}</p>
            {benefit.category && <div className="text-blue-800">{benefit.category}</div>}
            {benefit.validUntil && <div className="text-gray-700">Válido hasta: {new Date(benefit.validUntil).toLocaleDateString('es-ES')}</div>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BenefitDetailComponent;
