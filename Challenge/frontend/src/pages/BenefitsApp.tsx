import React, { useState, useEffect, useMemo, lazy, Suspense } from 'react';
import { Benefit } from '../types/Benefit';
import { FavoritesService } from '../services/FavoritesService';
import { mockBenefits } from '../mock/mockBenefits';
import BenefitCard from '../components/BenefitCard';

const BenefitDetailComponent = lazy(() => import('../components/BenefitDetailComponent'));

const BenefitsApp: React.FC = () => {
  const [benefits, setBenefits] = useState<Benefit[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all');
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedBenefit, setSelectedBenefit] = useState<Benefit | null>(null);
  const [favorites, setFavorites] = useState<number[]>([]);

  const itemsPerPage = 6;

  useEffect(() => {
    const loadBenefits = async () => {
      setLoading(true);
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulación de delay
      setBenefits(mockBenefits);
      setFavorites(FavoritesService.getFavorites());
      setLoading(false);
    };
    loadBenefits();
  }, []);

  const filteredBenefits = useMemo(() => {
    return benefits.filter(benefit => {
      const matchesSearch = benefit.name.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesStatus = statusFilter === 'all' || benefit.status === statusFilter;
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
      setFavorites(prev => prev.filter(fav => fav !== id));
    } else {
      FavoritesService.addFavorite(id);
      setFavorites(prev => [...prev, id]);
    }
  };

  useEffect(() => {
    setCurrentPage(1);
  }, [searchTerm, statusFilter]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p>Cargando beneficios...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto p-6">
          <h1 className="text-4xl font-bold">Beneficios Sport</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        {/* Filtros */}
        <div className="flex gap-4 mb-6">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Buscar beneficios..."
            className="border rounded px-3 py-2 flex-1"
          />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as 'all' | 'active' | 'inactive')}
            className="border rounded px-3 py-2"
          >
            <option value="all">Todos</option>
            <option value="active">Activos</option>
            <option value="inactive">Inactivos</option>
          </select>
        </div>

        {/* Grid de beneficios */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
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

        {/* Modal */}
        {selectedBenefit && (
          <Suspense fallback={<div>Cargando detalle...</div>}>
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
