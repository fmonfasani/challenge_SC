import { Heart } from 'lucide-react';
import { Link } from 'react-router-dom';

const BeneficioCard = ({ beneficio, isFavorite, toggleFavorite }) => {
  return (
    <div className="border rounded-lg p-4 flex flex-col justify-between shadow hover:shadow-lg transition">
      <img
        src={beneficio.imagen || 'https://via.placeholder.com/300x200'}
        alt={beneficio.nombre}
        className="h-40 w-full object-cover mb-4 rounded"
        loading="lazy"
      />
      <h2 className="text-lg font-bold mb-2">{beneficio.nombre}</h2>
      <p className="text-sm text-gray-600 mb-4">{beneficio.descripcion}</p>
      <div className="flex justify-between items-center mt-auto">
        <span className={`text-xs px-2 py-1 rounded-full ${beneficio.estado === 'activo' ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
          {beneficio.estado}
        </span>
        <button onClick={() => toggleFavorite(beneficio.id)}>
          <Heart color={isFavorite ? 'red' : 'gray'} fill={isFavorite ? 'red' : 'none'} />
        </button>
      </div>
      <Link to={`/beneficios/${beneficio.id}`} className="block mt-4 text-blue-600 hover:underline text-center">
        Ver Detalle
      </Link>
    </div>
  );
};

export default BeneficioCard;
