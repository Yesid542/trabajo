// App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import React from 'react';
import PantallaIncial from './components/pantallaIncial/pantallaInicial';
import IniciaSesion from './components/inicioSesion/inicioSesion';
import './App.css';

function App() {
  return (
    <BrowserRouter>
       <Routes>
         <Route path="/" element={<PantallaIncial/>}/>
         <Route path="/inciaSesion" element={<IniciaSesion/>}/>
       </Routes>
    </BrowserRouter>

  );
}

export default App;