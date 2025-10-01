import React, { use } from "react";
import { useState, useRef, useEffect} from "react";
import { supabase } from "../../../supabaseClient";
import './contenido.css';
import { data } from "react-router-dom";
import { Link } from "react-router-dom";


function contenido(){

    const [temas, setTemas] = useState([]);
    const [contenidoSupabase, setContenidoSupabase] = useState(null);
    const [contenido_temas, setContenidoTemas] = useState([]);


    const [activo, setActivo] = useState(false);
    const slidebarRef = useRef(null);

    const toggleSlidebar = (e) => {
    e.preventDefault();
    setActivo(prev => !prev);
  };


  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        slidebarRef.current &&
        !slidebarRef.current.contains(event.target) &&
        !event.target.closest('#activa')
      ) {
        setActivo(false);
      }
    };

    if (activo) {
      document.addEventListener('mousedown', handleClickOutside);
    } else {
      document.removeEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [activo]);


  const modulo = sessionStorage.getItem('modulo');

  
useEffect(() => {
  
    async function obtenerContenido() {
      const { data, error } = await supabase.from("contenido").select("*").eq("modulo", modulo);
;
      if (error) {
        console.error("Error al consultar:", error);
      } else {
        if (data.length>0) { 
          setContenidoSupabase(data);
          setTemas(data.sort((a, b) => a.idContenido - b.idContenido)
.map(tema => tema.titulo))
          setContenidoTemas(data)
          console.log(data)
        }
      }
    }
    obtenerContenido();
}, []);




useEffect(()=>{
  if (!contenidoSupabase) return;
    const title = document.getElementById("title");
    contenidoSupabase.forEach(item => {
      if(item.modulo == modulo){
        title.textContent = modulo
      }
    });
console.log(contenido_temas)
},[contenidoSupabase]);

    return(
        <div className="estructura">
            <header>
                <a href="#" id="activa" onClick={toggleSlidebar}>    
                    <div className="navegador">  
                        <svg id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" width='3vw' viewBox="0 0 25.35 11.94">

                          <g id="Capa_1-2" data-name="Capa 1">
                            <rect className="cls-300" x="0" y="0" width="25.35" height="2.94" rx="1.47" ry="1.47"/>
                            <rect className="cls-300" x="0" y="4.5" width="25.35" height="2.94" rx="1.47" ry="1.47"/>
                            <rect className="cls-300" x="0" y="9" width="25.35" height="2.94" rx="1.47" ry="1.47"/>
                          </g>
                        </svg>
                    </div>
                </a>
                <div className="buscador">
                    <input  type="text" name=""  id="buscador"></input>
                    <svg className="lupa" id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" width='25px' viewBox="0 0 13.83 17.04">
                      <g id="Capa_1-2" data-name="Capa 1">
                        <path className="cls-110" d="M13.71,15.61l-3.3-5.29c2.42-2.5,2.24-6.49-.35-8.78-.53-.47-1.15-.82-1.8-1.11L6.55.04C4.11-.29,1.19,1.56.4,3.89c-.18.52-.22,1.16-.39,1.69,0,.29-.01.58,0,.87.22,4.34,4.96,7.06,8.82,5.04l3.25,5.15c.77.95,2.16.05,1.64-1.03ZM10.17,8.9c-2.41,3.63-8.09,2.5-8.95-1.78C.56,3.84,3.37.73,6.69,1.22c3.66.54,5.55,4.55,3.48,7.67Z"/>
                      </g>
                    </svg>
                </div>
                <div className="accesibilidad">
                    
                    <div className="logro">
                        <img id="iconoLogro" src="../../../public/ICONS/Logro.svg" alt="" />
                    </div>
                    <div className="imgPerfil">
                        <div className="imagen"></div>
                    </div>
                </div>
            </header>
            <main className="content">
                <div className="figura-titulo">
                    <div className="figura">
                        <svg id="svgGrande" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" height='30.6vh' viewBox="0 0 1218.12 190.22">
                      <g id="Capa_1-2" data-name="Capa 1">
                        <path className="cls-301" d="M1519.81,167.67c-.21.16-.44.31-.67.45-21.31,12.56-110.85-15.26-136.14-17.62-26.86-2.5-54.49-.15-80.98,3.32-66.21,8.66-129.04,24.2-196.16,30.58-79.02,7.51-161.17,1.9-237.27-11.7-54.42-9.72-108.58-23.68-165.89-22.05-48,1.37-92.14,13.56-137.43,22.14-95.42,18.09-201.19,20.34-299.02,6.35-39.91-5.71-78.76-14.06-119.8-16.63-33.49-2.1-67.25-.23-100.35,2.73-22.01,1.96-42.71,8.56-44-5.87-4.72-52.87,0-106.43,0-159.38h1519.11c0,7.94,0,15.88,0,23.81,0,34.82,0,69.64,0,104.46,0,7.27,7.4,32.78-1.4,39.39Z"/>
                      </g>
                    </svg>
                    </div>
                    <div className="content-titulo"><h1 id="title" ></h1></div>
                    
                </div>

                {Object.entries(contenido_temas)
                .sort(([, a], [, b]) => a.idContenido - b.idContenido)
                .map(([clave, tema], indexs) => (
                <div
                  key={indexs}
                  className="contenidos"
                  style={{
                    top: `${indexs * 200}px`, // separa verticalmente cada bloque
                    position: 'absolute',
                    width: '80vw',
                    marginLeft: '10vw'
                  }}
                >
                  <h3 style={{display:"flex",justifyContent:"center"}} >{tema.titulo}</h3>
                  <p>{tema.contenido}</p>
                </div>
              ))}


                <div className="barra-navegacion">
                    <div className="boton-izquierdo">
                        <svg id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" width='40px' viewBox="0 0 10.1 6.03">
                          <g id="Capa_1-2" data-name="Capa 1">
                            <g>
                              <rect className="cls-302" x=".12" y="2.5" width="9.98" height="1.13" rx=".57" ry=".57" transform="translate(10.22 6.12) rotate(180)"/>
                              <rect className="cls-302" x="-.36" y="1.18" width="4.48" height="1.14" rx=".57" ry=".57" transform="translate(4.46 1.66) rotate(135)"/>
                              <rect className="cls-302" x="-.48" y="3.64" width="4.48" height="1.23" rx=".62" ry=".62" transform="translate(3.53 0) rotate(45)"/>
                            </g>
                          </g>
                        </svg>
                    </div>
                    <div className="barra"></div>
                    <div className="boton-derecho">
                        <svg id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" width='40px' viewBox="0 0 10.1 6.03">
                          <g id="Capa_1-2" data-name="Capa 1">
                            <g>
                              <rect className="cls-302" x="0" y="2.5" width="9.98" height="1.13" rx=".57" ry=".57"/>
                              <rect className="cls-302" x="5.97" y="1.18" width="4.48" height="1.14" rx=".57" ry=".57" transform="translate(3.64 -5.29) rotate(45)"/>
                              <rect className="cls-302" x="6.09" y="3.64" width="4.48" height="1.23" rx=".62" ry=".62" transform="translate(17.24 1.38) rotate(135)"/>
                            </g>
                          </g>
                        </svg>
                    </div>
                </div>
            </main>
            <div ref={slidebarRef} className={`slidebar ${activo ? 'activa' : ''}`}>
              <div className="slideNav">
                <Link to={"/principal"}> 
                  <img className="slideHome" src="../../../public/ICONS/slideHome.svg"  alt="" />
                  <span className="linea">___________</span>
                </Link>
              </div>
                {temas.map((tema, index) => (
                  <div key={index} className="nav">{tema}</div>
                    ))}
            </div>
        </div>
    )
    
}
export default contenido;