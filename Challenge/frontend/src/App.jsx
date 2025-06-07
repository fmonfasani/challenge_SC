import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import BeneficiosList from './components/BeneficiosList';
import BeneficioDetail from './components/BeneficioDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/beneficios" element={<BeneficiosList />} />
        <Route path="/beneficios/:id" element={<BeneficioDetail />} />
        <Route path="*" element={<div className="p-4">404 - Página no encontrada</div>} />
      </Routes>
    </Router>
  );
}

export default App;
