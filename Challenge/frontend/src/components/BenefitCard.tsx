import React, { useState } from 'react';
import { Benefit } from '../types/Benefit';

interface BenefitCardProps {
  benefit: Benefit;
  onSelect: (benefit: Benefit) => void;
  isFavorite: boolean;
  onToggleFavorite: (id: number) => void;
}

const BenefitCard: React.FC<BenefitCardProps> = ({ benefit, onSelect, isFavorite, onToggleFavorite }) => {
  const [imageLoaded, setImageLoaded] = useState(false);

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-all hover:scale-105 cursor-pointer">
      <div className="relative h-48 bg-gray-200">
        <img
          src={benefit.image}
          alt={benefit.name}
          className={`w-full h-full object-cover transition-opacity duration-300 ${imageLoaded ? 'opacity-100' : 'opacity-0'}`}
          onLoad={() => setImageLoaded(true)}
          loading="lazy"
        />
        <button
          onClick={(e) => {
            e.stopPropagation();
            onToggleFavorite(benefit.id);
          }}
          className="absolute top-2 right-2 p-2 bg-white rounded-full shadow-md hover:bg-gray-50"
        >
          <svg
            className={`w-5 h-5 ${isFavorite ? 'text-red-500 fill-current' : 'text-gray-400'}`}
            fill={isFavorite ? 'currentColor' : 'none'}
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
        </button>
      </div>
      <div className="p-4" onClick={() => onSelect(benefit)}>
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-900 truncate">{benefit.name}</h3>
          <span className={`px-2 py-1 rounded-full text-xs font-medium ${benefit.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
            {benefit.status === 'active' ? 'Activo' : 'Inactivo'}
          </span>
        </div>
        <p className="text-gray-600 text-sm line-clamp-2">{benefit.description}</p>
      </div>
    </div>
  );
};

export default BenefitCard;
