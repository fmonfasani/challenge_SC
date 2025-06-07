import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getBeneficioById } from '../services/api';

const BeneficioDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [beneficio, setBeneficio] = useState(null);

  useEffect(() => {
    getBeneficioById(id).then((data) => setBeneficio(data));
  }, [id]);

  if (!beneficio) {
    return <div>Cargando...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <button onClick={() => navigate(-1)} className="mb-4 text-blue-600 hover:underline">
        Volver
      </button>
      <div className="flex flex-col items-center">
        <img
          src={beneficio.imagen || 'https://via.placeholder.com/300x200'}
          alt={beneficio.nombre}
          className="h-60 w-full object-cover mb-4 rounded"
          loading="lazy"
        />
        <h1 className="text-2xl font-bold mb-2">{beneficio.nombre}</h1>
        <p className="text-gray-600 mb-4">{beneficio.descripcion}</p>
        <span className={`text-sm px-4 py-2 rounded-full ${beneficio.estado === 'activo' ? 'bg-green-200 text-green-800' : 'bg-red-200 text-red-800'}`}>
          {beneficio.estado}
        </span>
      </div>
    </div>
  );
};

export default BeneficioDetail;
