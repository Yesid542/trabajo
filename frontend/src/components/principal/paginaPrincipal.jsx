import React, { useRef, useEffect} from "react";
import "./paginaPrincipal.css";
import { data } from "react-router-dom";


function PaginaPrincipal(){
  const introduccionRef = useRef(null);
  const fundamentosRef = useRef(null);
  const estructurasDatosIRef = useRef(null);
  const estructurasDatosIIRef = useRef(null);
  const estructurasControlIRef = useRef(null);
  const estructurasControlIIRef = useRef(null);
  const descripcion = '';
  const reciente = document.getElementById("reciente");
  const textoDescripcion = document.getElementById("moduloDescripcion");
  const opciones = document.querySelectorAll(".modulo");

  opciones.forEach(opcion =>{
    opcion.addEventListener("click", ()=> {
      reciente.style.backgroundImage = `url(${opcion.dataset.img})`;
      textoDescripcion.textContent = opcion.dataset.texto;
    });
})

  
useEffect(() => {

    fetch('http://127.0.0.1:5000/api/rutas')
    .then(respuesta => {
      if (!respuesta.ok) {
        throw new Error(`Error HTTP: ${respuesta.status}`);
      }
      return respuesta.json(); // ← esto sigue siendo una promesa
    })
    .then(dataRutas => {
      console.log("Rutas recibidas:", dataRutas);

    
        for( const ruta of dataRutas.rutas){
          if (ruta.tabla && ruta.idRegistro){
            fetch(`http://127.0.0.1:5000/api/${ruta.tabla}/${ruta.idRegistro}`)
            .then(res=>{
              if (!res.ok) {
                throw new Error(`Error HTTP: ${res.status}`); 
              }
              return res.json(); 
            })
          .then(dataModulos=>{
            console.log('respuesta',dataModulos);

            const modulo = dataModulos.data;
            if( introduccionRef.current && modulo.nombre == introduccionRef.current.id){
              const imagenIntroduccion = ruta.rutaSupabase; 
              const introduccion = document.getElementById("Introduccion");
              introduccion.dataset.img = imagenIntroduccion;
              introduccion.style.backgroundImage = `url(${introduccion.dataset.img})`
              } 
            if(fundamentosRef.current && modulo.nombre == fundamentosRef.current.id){
              const imagenFundamentos = ruta.rutaSupabase; 
              fundamentosRef.current.style.backgroundImage=`url(${imagenFundamentos})`
              }
            if(estructurasDatosIRef.current && modulo.nombre == estructurasDatosIRef.current.id){
              const imagenEstructuraDatosI = ruta.rutaSupabase; 
              estructurasDatosIRef.current.style.backgroundImage=`url(${imagenEstructuraDatosI})`
              const imagenEstructuraDatosII = ruta.rutaSupabase; 
              estructurasDatosIIRef.current.style.backgroundImage=`url(${imagenEstructuraDatosII})`
              }
            if(estructurasControlIRef.current && modulo.nombre == estructurasControlIRef.current.id){
              const imagenEstructurasControlI = ruta.rutaSupabase; 
              estructurasControlIRef.current.style.backgroundImage=`url(${imagenEstructurasControlI})`
              const imagenEstructurasControlII = ruta.rutaSupabase; 
              estructurasControlIIRef.current.style.backgroundImage=`url(${imagenEstructurasControlII})`
            }
          }
          )
          .catch(error => {
            console.error("Error al obtener los modulos:", error);
          });

          }
        }
      })

    .catch(error => {
      console.error("Error al obtener las rutas:", error);
    });


  }, []);

  
    
  

return(
    <div className="cuerpo">
        <header className="superior">
          <div className="logoSer">
            <img className="serkana" src="../../../public/ICONS/Serkana.svg" alt="Logo de la empresa" width="100" ></img>
          </div>
          <div className="buscar">
            <input  type="text" name=""  id="buscador"></input>
            <svg className="lupa" id="Capa_2" data-name="Capa 2" xmlns="http://www.w3.org/2000/svg" width='25px' viewBox="0 0 13.83 17.04">
              <g id="Capa_1-2" data-name="Capa 1">
                <path className="cls-110" d="M13.71,15.61l-3.3-5.29c2.42-2.5,2.24-6.49-.35-8.78-.53-.47-1.15-.82-1.8-1.11L6.55.04C4.11-.29,1.19,1.56.4,3.89c-.18.52-.22,1.16-.39,1.69,0,.29-.01.58,0,.87.22,4.34,4.96,7.06,8.82,5.04l3.25,5.15c.77.95,2.16.05,1.64-1.03ZM10.17,8.9c-2.41,3.63-8.09,2.5-8.95-1.78C.56,3.84,3.37.73,6.69,1.22c3.66.54,5.55,4.55,3.48,7.67Z"/>
              </g>
            </svg>
          </div>
          <div className="perfil">
            <div className="user"></div>
          </div>
        </header>
        <div className="layout">
          <aside className="lateral">
            <div className="icono">
              <img className="home" src="../../../public/ICONS/Home.svg"  alt="" />
              <p className="texto" >Inicio</p>
            </div>
            <div className="iconos">
              <img id="aprendices" src="../../../public/ICONS/aprendices.svg" alt="" />
  
              <p className="texto" >Aprendices</p>
            </div>
            <div className="iconos">
              <img id="instructores" src="../../../public/ICONS/instructores.svg" alt="" />
              <p className="texto" >Instructores</p>
            </div>
            <div className="logros">
              <img id="logros" src="../../../public/ICONS/Logros.svg" alt="" />
              <p className="texto" >Logros</p>
              </div>
            <div className="ajustes">
              <img id="ajustes" src="../../../public/ICONS/Ajustes.svg" alt="" />
              <p className="texto" >Ajustes</p>
            </div>
          </aside>
          <main>
            <button className="filtro-primero">Basico</button>
            <button className="filtro" >Intermedio</button>
            <button className="filtro" >Avanzado</button>
            <div className="Bienvenida">
              <img className="estrella-bienvenida" src="../../../public/ICONS/Estrella.svg" alt="Logo de la empresa" width="40" ></img>
              <p className="saludo">Hola Cristiano</p>
            </div>
            <div className="grupo">
              <a href="">
              <div className="reciente" id="reciente">
                <div className="barra_progreso">
                  <div className="progreso" style={{width: '60%'}}></div> 
                </div>
                <img className="estrella" src="../../../public/ICONS/Estrella.svg" alt="Logo de la empresa" width="100" ></img>
              </div>
              </a>
              <div className="descripcion">
                <div className="contenido">
                  <p id="moduloDescripcion">{descripcion}</p>
                </div>
                <p className="titulo">Introduccion</p>
              </div>
            </div>
            <div className="etiquetas">
              <p className="etiqueta">Nivel 1 <strong id="nivel">(Basico)</strong> </p>
            </div>
            <div className="modulos">
              <div className="introduccion modulo" id="Introduccion" ref={introduccionRef}>
                <div className="titulo-modulo">Introduccion</div>
              </div>
              <div className="modulo" id="Fundamentos" ref={fundamentosRef} >
                <div className="titulo-modulo">Fundamentos del lenguaje</div>
              </div>
              <div className="modulo" id="EstructurasDatosI" ref={estructurasDatosIRef} >
                <div className="titulo-modulo">Estructuras de datos I</div>
              </div>
              <div className="modulo" id="EstructurasDatosII" ref={estructurasDatosIIRef}  >
                <div className="titulo-modulo">Estructuras de datos II</div>
              </div>
              <div className="modulo" id="EstructurasControlI" ref={estructurasControlIRef}  >
                <div className="titulo-modulo">Estructuras de Control I</div>
              </div>
            </div>
            <div className="etiquetas">
              <p className="etiqueta">Nivel 2 <strong id="nivel">(Intermedio)</strong> </p>
            </div>
            <div className="modulos">
              <div className="introduccion modulo" id="EstructurasControlII" ref={estructurasControlIIRef} >
                <div className="titulo-modulo">Estructuras de control II</div>
              </div>
              <div className="modulo" ></div>
              <div className="modulo" ></div>
              <div className="modulo" ></div>
              <div className="modulo" ></div>
            </div>
            <div className="etiquetas">
              <p className="etiqueta">Nivel 3 <strong id="nivel">(Avanzado)</strong> </p>
            </div>
            <div className="modulos">
              <div className="introduccion modulo" >
                <div className="titulo-modulo">Introduccion</div>
              </div>
              <div className="modulo" ></div>
              <div className="modulo" ></div>
              <div className="modulo" ></div>
              <div className="modulo" ></div>
            </div>
          </main>
        </div>
        
    </div>
)
}
export default PaginaPrincipal