import { useState } from 'react';
import '../inicioSesion/inicioSesion.css'; // Estilos opcionales

function PasswordInput() {
  const [showPassword, setShowPassword] = useState(false);

  const togglePassword = () => setShowPassword(prev => !prev);
  return(
    <div className="input-password">
                  <input className='contrasena'
                    type={showPassword ? 'text' : 'password'}
                    placeholder="Contraseña"
                    id='contrasena'
                  />
                  <span className="icon" onClick={togglePassword}>
                    {showPassword ? (
                      <svg id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" width='20px' viewBox="0 0 13.62 7.82">
                       <g id="Capa_1-2" data-name="Capa 1">
                         <path className="cls-6" d="M6.68,2.44c-1.49,0-2.69,1.2-2.69,2.69s1.2,2.69,2.69,2.69,2.69-1.2,2.69-2.69-1.2-2.69-2.69-2.69ZM6.68,6.7c-.87,0-1.58-.71-1.58-1.58s.71-1.58,1.58-1.58,1.58.71,1.58,1.58-.71,1.58-1.58,1.58Z"/>
                         <path className="cls-6" d="M.29,5.78c-.29-.11-.37-.56-.22-.87C.96,3.1,2.34,1.36,4.24.55,5.18.15,6.22-.04,7.24,0c1.03.05,2.07.42,2.94.97.59.38,1.14.84,1.62,1.36.69.74,1.42,1.55,1.74,2.53.06.18.1.38.06.57-.09.37-.55.49-.82.21-.12-.12-.19-.28-.25-.44-.56-1.26-1.43-2.39-2.57-3.16-2-1.34-4.52-1.22-6.47.14-.09.06-.17.12-.26.19-.58.45-1.08.99-1.47,1.61-.21.32-.37.65-.53,1-.13.29-.26.67-.59.79-.14.05-.25.05-.34.01Z"/>
                       </g>
                  </svg>
                    ) : (
                      <svg id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" width='20px' viewBox="0 0 13.63 11.09">
                        <g id="Capa_1-2" data-name="Capa 1">
                          <path className="cls-6" d="M13.61,6.73c-.05-.22-.31-.7-.43-.92-.67-1.22-1.63-2.32-2.79-3.1l1.89-1.94c.26-.5-.34-1-.78-.65l-2.07,2.06c-1.66-.74-3.52-.75-5.19-.03-1.62.7-2.99,2.13-3.82,3.66-.21.39-.79,1.34-.13,1.58.3.11.54-.03.68-.3.35-.66.55-1.18,1.01-1.8,1.58-2.11,4.03-3.23,6.64-2.34l-.05.1-1.33,1.33c-1.45-.26-2.9.83-3.01,2.3-.02.23.02.46.02.69l-2.91,2.92c-.32.48.26,1.03.73.7l2.59-2.59h.05c.85,1.21,2.58,1.45,3.71.5,1.33-1.12,1.21-3.08-.16-4.1l1.33-1.32c.08-.02.67.44.78.52.74.61,1.45,1.5,1.9,2.35.13.25.22.54.35.77.32.59,1.11.29.96-.39ZM5.47,7.61l2.03-2.03c.22-.06.67.59.74.79.66,1.8-1.91,2.93-2.77,1.25Z"/>
                        </g>
                      </svg>
                    )}
                  </span>
                </div>
  )
}

export default PasswordInput