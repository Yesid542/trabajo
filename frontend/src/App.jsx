// App.jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import React from 'react';
import IniciaSesion from './components/inicioSesion/inicioSesion';
import LogoInicio from './components/logoInicio/logoInicio';
import Registro from './components/registro/registrarse';
import Principal from './components/principal/paginaPrincipal';
import Contenidos from './components/contenido/contenido';
import './App.css'

function App() {
  return (
    <BrowserRouter>
       <Routes>
         <Route path="/" element={<LogoInicio/>}/>
         <Route path="/inicia" element={<IniciaSesion/>}/>
         <Route path="/registrar" element={<Registro/>}/>
         <Route path='/principal' element={<Principal/>}/>
         <Route path='/contenidos' element={<Contenidos/>}/>
       </Routes>
    </BrowserRouter>

  );
}

export default App;