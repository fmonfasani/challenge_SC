import { useEffect, useState } from 'react';

interface Beneficio {
  id: number;
  nombre: string;
  descripcion: string;
  estado: string;
  imagen?: string;
}

function App() {
  const [beneficios, setBeneficios] = useState<Beneficio[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_API_URL}/beneficios`)
      .then((response) => response.json())
      .then((data) => {
        setBeneficios(data.beneficios || []);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching beneficios:', error);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading beneficios...</p>;

  return (
    <div>
      <h1>Lista de Beneficios</h1>
      <ul>
        {beneficios.map((beneficio) => (
          <li key={beneficio.id}>
            <strong>{beneficio.nombre}</strong> - {beneficio.estado}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
