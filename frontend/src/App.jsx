// App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import React from 'react';
import IniciaSesion from './components/inicioSesion/inicioSesion';
import LogoInicio from './components/logoInicio/logoInicio';
import Registro from './components/registro/registrarse';
import './App.css'

function App() {
  return (
    <BrowserRouter>
       <Routes>
         <Route path="/inicio" element={<LogoInicio/>}/>
         <Route path="/" element={<IniciaSesion/>}/>
         <Route path="/registrar" element={<Registro/>}/>
       </Routes>
    </BrowserRouter>

  );
}

export default App;