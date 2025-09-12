import React from "react";
import './registrarse.css'
import '../../../public/fonts/fonts.css'
import { useState } from "react";


function Registrar(){
   const [ficha, setFicha] = useState('');
  const [errorFicha, setErrorFicha] = useState('');
  const [fichaVerified, setFichaVerified] = useState(false);
  

  // Función para verificar la ficha
  const verificarFicha = async (numeroFicha) => {
    setErrorFicha('');
    
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/fichas/valida/${numeroFicha}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });
      
      if (!response.ok) {
        throw new Error('Error en la respuesta del servidor');
      }
      
      const data = await response.json();
      console.log("Respuesta del servidor:", data); 
      
      if (data.existe) {
        setErrorFicha('');
        setFichaVerified(true);
        return true;
      } else {
        setErrorFicha('La ficha ingresada no existe');
        setFichaVerified(false);
        return false;
      }
    } catch (error) {
      console.error('Error:', error);
      setErrorFicha('Error al verificar la ficha');
      setFichaVerified(false);
      return false;
    }
  };

  const crearUsuario= async(nombre, apellido, tipoDocumento, documento,idFicha, correo, contrasena ) => {
    try{
      const respuesta = await fetch(`http://127.0.0.1:5000/api/usuarios`,{
        method:'POST',
        headers: {
          'Content-Type':'application/json',
        },
      });

      if (!respuesta.ok) {
        throw new Error('Error en la respuesta del servidor');
      }

    }catch{

    }

  }

  
  // Manejar cambio en el input
 const handleSubmit = async (e) => {
  e.preventDefault();

  const fichaSanitizada = ficha.replace(/\D/g, '');

  const esValida = await verificarFicha(fichaSanitizada);

  if (esValida) {
    console.log("ficha bien");
  } 

};

    return(
        <div className="areaM" style={{fontFamily:'WorkSans-Medium'}} >
            <div className="formulario">
                <svg className="appR" id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 112.75 102">
   
                  <g id="Capa_1-2" data-name="Capa 1">
                    <g>
                      <rect className="cls-3" width="112.75" height="98.09" rx="15.2" ry="15.2"/>
                      <path className="cls-2" d="M79.02,63.57c-1.45,2.92-4.43,4.77-7.7,4.77h-25.72c-3.06,0-5.89-1.63-7.43-4.28L8.49,12.9C5.16,7.18,9.3,0,15.92,0h80.79c6.38,0,10.53,6.7,7.7,12.41l-25.39,51.16Z"/>
                      <polygon className="cls-1" points="65 102 65 68.35 51.7 68.35 51.7 102 58.35 92.9 65 102"/>
                      <ellipse className="cls-1" cx="90.87" cy="42.63" rx="12.24" ry="5.9" transform="translate(2.61 90.43) rotate(-53.57)"/>
                      <ellipse className="cls-1" cx="23.19" cy="42.63" rx="5.9" ry="12.24" transform="translate(-20.78 22.1) rotate(-36.43)"/>
                    </g>
                  </g>
                </svg>
                <h1 className="tituloR"style={{fontFamily:'WorkSans-Bold' }}  >Regístrate</h1>
                <svg className="logoR" id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 473.37 98.03">
                  <g id="Capa_1-2" data-name="Capa 1">
                    <g>
                      <path className="cls-1" d="M65.49,33.2c-3.3,0-6.41.63-9.32,1.9-2.92,1.27-5.45,3.02-7.59,5.28-2.15,2.26-3.85,4.84-5.11,7.75-1.27,2.92-1.9,6.02-1.9,9.32-.11,5.61-1.27,10.86-3.47,15.76-2.2,4.89-5.2,9.18-8.99,12.87-3.79,3.68-8.19,6.6-13.19,8.74-5.01,2.15-10.31,3.22-15.92,3.22v-17.65c3.3,0,6.41-.63,9.32-1.9,2.91-1.26,5.44-2.97,7.59-5.11,2.15-2.14,3.85-4.67,5.11-7.59,1.26-2.91,1.9-6.02,1.9-9.32.11-5.61,1.24-10.89,3.38-15.84,2.15-4.95,5.06-9.29,8.74-13.03,3.68-3.74,8-6.68,12.95-8.82,4.95-2.15,10.23-3.22,15.84-3.22l.66,17.65Z"/>
                      <path className="cls-1" d="M97.34,81.82c2.59,0,5.04-.5,7.33-1.49,2.29-.99,4.3-2.34,6.03-4.02,1.73-1.69,3.09-3.67,4.09-5.97.99-2.29,1.49-4.78,1.49-7.46h13.5c0,4.5-.85,8.72-2.53,12.65-1.69,3.94-4.01,7.38-6.94,10.31-2.94,2.94-6.38,5.26-10.31,6.94-3.94,1.69-8.15,2.53-12.65,2.53s-8.72-.84-12.65-2.53c-3.94-1.69-7.38-4-10.32-6.94-2.94-2.94-5.26-6.38-6.94-10.31-1.69-3.93-2.53-8.15-2.53-12.65s.84-8.71,2.53-12.65c1.68-3.94,4-7.37,6.94-10.31,2.94-2.94,6.38-5.26,10.32-6.94,3.93-1.69,8.15-2.53,12.65-2.53s8.52.8,12.32,2.4c3.81,1.6,7.18,3.79,10.12,6.55l.26.26,8.82,9.08-14.53,14.4h-17.91l13.89-14.27c-1.64-1.47-3.59-2.66-5.84-3.57-2.25-.91-4.63-1.36-7.14-1.36s-5.04.5-7.33,1.49c-2.29,1-4.3,2.36-6.03,4.09-1.73,1.73-3.09,3.74-4.09,6.03-1,2.29-1.49,4.74-1.49,7.33s.49,5.04,1.49,7.33c.99,2.29,2.35,4.3,4.09,6.03,1.73,1.73,3.74,3.09,6.03,4.09,2.29,1,4.74,1.49,7.33,1.49Z"/>
                      <path className="cls-1" d="M142.63,62.88c-.09-4.41.71-8.58,2.4-12.52,1.69-3.93,4-7.37,6.94-10.31,2.94-2.94,6.4-5.27,10.38-7.01,3.98-1.73,8.22-2.6,12.72-2.6v13.5c-2.6,0-5.04.5-7.33,1.49-2.29,1-4.3,2.34-6.03,4.02-1.73,1.69-3.09,3.7-4.09,6.03-1,2.34-1.49,4.8-1.49,7.4v32.44h-13.49v-32.44Z"/>
                      <path className="cls-1" d="M226.96,52.76c4.41,3.03,7.93,6.92,10.57,11.68,2.64,4.76,3.87,9.91,3.7,15.44v15.44h-13.37v-15.44c0-2.6-.5-5.04-1.49-7.33-.99-2.29-2.36-4.3-4.09-6.03-1.73-1.73-3.76-3.09-6.1-4.09-2.33-.99-4.84-1.49-7.53-1.49h-8.04v34.38h-13.24V13.57L200.62.08v47.23h5.06c2.6,0,5.04-.5,7.33-1.49,2.29-.99,4.3-2.33,6.04-4.02,1.73-1.69,3.09-3.7,4.09-6.03.99-2.34,1.49-4.8,1.49-7.4h13.49c0,4.93-1.02,9.5-3.05,13.69-2.04,4.2-4.74,7.77-8.11,10.71Z"/>
                      <path className="cls-1" d="M285.09,95.32c-4.5,0-8.71-.86-12.65-2.6-3.94-1.73-7.37-4.07-10.32-7.01-2.94-2.94-5.25-6.38-6.94-10.31-1.69-3.94-2.53-8.11-2.53-12.52s.84-8.71,2.53-12.65c1.69-3.94,4-7.37,6.94-10.31,2.94-2.94,6.38-5.26,10.32-6.94,3.94-1.69,8.15-2.53,12.65-2.53s8.71.84,12.65,2.53c3.94,1.69,7.37,4,10.32,6.94,2.94,2.94,5.25,6.38,6.94,10.31s2.53,8.15,2.53,12.65v32.44h-13.49v-32.44c0-2.68-.5-5.19-1.49-7.53-1-2.34-2.36-4.37-4.09-6.1-1.73-1.73-3.74-3.09-6.03-4.09-2.29-.99-4.74-1.49-7.33-1.49s-5.04.5-7.33,1.49c-2.29,1-4.3,2.36-6.04,4.09-1.73,1.73-3.09,3.76-4.08,6.1-1,2.33-1.5,4.85-1.5,7.53s.5,5.04,1.5,7.33c.99,2.29,2.35,4.3,4.08,6.03,1.73,1.73,3.74,3.09,6.04,4.09,2.29,1,4.73,1.49,7.33,1.49.86,0,1.66-.04,2.4-.13s1.49-.21,2.27-.39l3.11,13.11c-3.9.6-6.49.91-7.79.91Z"/>
                      <path className="cls-1" d="M396.68,95.32h-13.49v-32.44c0-2.6-.5-5.06-1.49-7.4-1-2.34-2.36-4.35-4.09-6.03-1.73-1.69-3.74-3.03-6.03-4.02-2.29-.99-4.74-1.49-7.33-1.49s-5.04.5-7.33,1.49c-2.29,1-4.3,2.34-6.04,4.02-1.73,1.69-3.09,3.7-4.09,6.03-.99,2.34-1.49,4.8-1.49,7.4v32.44h-13.49v-32.44c-.09-4.41.72-8.58,2.4-12.52,1.69-3.93,4-7.37,6.94-10.31,2.94-2.94,6.4-5.27,10.38-7.01,3.98-1.73,8.22-2.6,12.72-2.6s8.74.87,12.72,2.6c3.98,1.73,7.44,4.07,10.38,7.01,2.94,2.94,5.26,6.38,6.94,10.31,1.68,3.94,2.49,8.11,2.4,12.52v32.44Z"/>
                      <path className="cls-1" d="M440.93,95.32c-4.5,0-8.71-.86-12.65-2.6-3.94-1.73-7.37-4.07-10.32-7.01-2.94-2.94-5.25-6.38-6.94-10.31-1.69-3.94-2.53-8.11-2.53-12.52s.84-8.71,2.53-12.65c1.69-3.94,4-7.37,6.94-10.31,2.94-2.94,6.38-5.26,10.32-6.94,3.94-1.69,8.15-2.53,12.65-2.53s8.71.84,12.65,2.53c3.94,1.69,7.37,4,10.32,6.94,2.94,2.94,5.25,6.38,6.94,10.31,1.69,3.94,2.53,8.15,2.53,12.65v32.44h-13.49v-32.44c0-2.68-.5-5.19-1.49-7.53-1-2.34-2.36-4.37-4.09-6.1-1.73-1.73-3.74-3.09-6.03-4.09-2.29-.99-4.74-1.49-7.33-1.49s-5.04.5-7.33,1.49c-2.29,1-4.3,2.36-6.04,4.09-1.73,1.73-3.09,3.76-4.08,6.1-1,2.33-1.5,4.85-1.5,7.53s.5,5.04,1.5,7.33c.99,2.29,2.35,4.3,4.08,6.03,1.73,1.73,3.74,3.09,6.04,4.09,2.29,1,4.73,1.49,7.33,1.49.86,0,1.66-.04,2.4-.13s1.49-.21,2.27-.39l3.11,13.11c-3.9.6-6.49.91-7.79.91Z"/>
                      <polygon className="cls-1" points="224.61 28.42 224.55 0 230.79 11.98 237.85 1.13 238.12 28.37 224.61 28.42"/>
                    </g>
                  </g>
                </svg>
                <div className="ingresa">
                    <form onSubmit={handleSubmit} className="regi" action="">
                        <div className="col">
                            <label htmlFor="">Nombre</label>
                            <input type="text" className="inText" required />
                            <label htmlFor="">Tipo de Documento</label>
                            <select className="inSelect" name="" id="">
                              <option value="">CC</option>
                              <option value="">TI</option>
                              <option value="">CE</option>
                              <option value="">PASAPORTE</option>
                            </select><br />
                            <label htmlFor="">Ficha</label>
                             <input 
                               type="text" 
                               id="ficha"
                               className={`inText ${errorFicha ? 'error' : ''} ${fichaVerified ? 'success' : ''}`}
                               value={ficha}
                               onChange={(e) => setFicha(e.target.value.replace(/\D/g, ''))}
                               maxLength={10} // Ajusta según necesidad
                             />
                             
                              {errorFicha && (
                              <span className={`error-text ${fichaVerified ? 'success-text' : ''}`}>
                                {errorFicha}
                              </span>
                            )}
                            <label htmlFor="">Crea tu contraseña</label>
                            <input type="text" className="inText" />
                        </div>
                        <div className="col">
                            <label htmlFor="">Apellido</label>
                            <input type="text" className="inText" required />
                            <label htmlFor="">N° Documento</label>
                            <input type="text" className="inText" required/>
                            <label htmlFor="">Email</label>
                            <input type="text" className="inText"  required/>
                            <label htmlFor="">Confirma tu contraseña</label>
                            <input type="text" className="inText" required />
                        </div>

                        <button className="guardar"style={{fontFamily:'WorkSans-Medium' }} type="submit" >Crear Cuenta</button>
                    </form>

                </div>

            
            </div>

        </div>
    )
  }
export default Registrar