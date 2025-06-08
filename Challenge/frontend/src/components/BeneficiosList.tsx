import { useState, useEffect } from 'react';
import { getBeneficios, Beneficio } from '../services/api';
import BeneficioCard from './BeneficioCard';

const BeneficiosList: React.FC = () => {
  const [beneficios, setBeneficios] = useState<Beneficio[]>([]);
  const [search, setSearch] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('todos');
  const [favorites, setFavorites] = useState<number[]>(() => {
    const favs = localStorage.getItem('favoritos');
    return favs ? JSON.parse(favs) : [];
  });

  useEffect(() => {
    getBeneficios().then((data) => {
      setBeneficios(data.beneficios);
    });
  }, []);

  const toggleFavorite = (id: number) => {
    let updatedFavorites;
    if (favorites.includes(id)) {
      updatedFavorites = favorites.filter(favId => favId !== id);
    } else {
      updatedFavorites = [...favorites, id];
    }
    setFavorites(updatedFavorites);
    localStorage.setItem('favoritos', JSON.stringify(updatedFavorites));
  };

  const filteredBeneficios = beneficios.filter((b) => {
    const matchesSearch = b.nombre.toLowerCase().includes(search.toLowerCase());
    const matchesStatus = filterStatus === 'todos' || b.estado === filterStatus;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="container mx-auto p-4">
      <div className="flex flex-col sm:flex-row justify-between mb-4 gap-4">
        <input
          type="text"
          placeholder="Buscar beneficio..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="p-2 border rounded w-full sm:w-1/2"
        />
        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value)}
          className="p-2 border rounded w-full sm:w-1/4"
        >
          <option value="todos">Todos</option>
          <option value="activo">Activo</option>
          <option value="inactivo">Inactivo</option>
        </select>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredBeneficios.map((beneficio) => (
          <BeneficioCard
            key={beneficio.id}
            beneficio={beneficio}
            isFavorite={favorites.includes(beneficio.id)}
            toggleFavorite={toggleFavorite}
          />
        ))}
      </div>
    </div>
  );
};

export default BeneficiosList;

