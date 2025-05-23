import React, { useState, useRef, useEffect } from "react";
import styled from "styled-components";
import jsPDF from "jspdf";
import html2canvas from "html2canvas";
import { FaFilePdf } from "react-icons/fa";
const FaFilePdfIcon = FaFilePdf as unknown as React.FC<{ size?: number }>;

type TaskResultsProps = {
  taskResult: { [key: string]: any };
  image: File;
};

const TaskResultsWrapper = styled.div`
  width: 100%;
  position: relative;
  font-family: 'Montserrat', sans-serif;
  padding: 40px 20px;

  
  .laptop {
    position: relative;
    max-width: 1300px;
    margin: auto;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    overflow: hidden;
  }

  .header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #D6E6FF;
    padding: 10px 20px;
    border-radius: 8px 8px 0 0;
  }

  .dot {
    height: 12px;
    width: 12px;
    background-color: #bbb;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
  }

  .content {
    background-image: url("/background.png");
    background-size: contain;
    height: 70vh;
    width: 100%;  
    border-radius: 0 0 10px 10px;
    font-size: 16px;
    box-sizing: border-box;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 0 20px;
  }

  .content-inner {
    padding: 20px 0 40px;
  }

  .uploaded-image-wrapper {
    max-width: 900px;
    margin: 20px auto;
    background: rgb(0, 0, 0);
    padding: 2px;
    border-radius: 16px;
    border:1px solid;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .uploaded-image {
    width: 100%;
    border-radius: 12px;
    object-fit: cover;
    border: 1px solid;
  }
    

  .result-grid {
    border:1px solid;
    display: grid;
    grid-template-columns: 1fr 2fr;
    row-gap: 20px;
    column-gap: 20px;
    max-width: 850px;
    margin: 20px auto;
    padding: 24px;
    background: #ffffff;
    border-radius: 16px;
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.08);
  }

  .result-label {
    font-weight: 600;
    color: #374151;
    font-size: 16px;
    text-align: right;
  }

  .result-value {
    font-weight: 500;
    color: #111827;
    font-size: 16px;
  }

  .download-button {
    background: white;
    color: #e11d48;
    border: 1px solid #e11d48;
    padding: 10px 20px;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
  }

  .download-button:hover {
    background: #e11d48;
    color: white;
  }
`;

const HEADER_TEXT = "IMAGEN";
const FOOTER_TEXT = "Si estás conforme con esta clasificación, presiona el botón “Confirmar”. Si detectas algún error ajusta la clase manualmente.";
const now = new Date();
const fecha = now.toLocaleDateString("es-ES"); // "23/05/2025"
const hora = now.toLocaleTimeString("es-ES", { hour: '2-digit', minute: '2-digit' }); // "16:42"

const clasificadoEn = `${hora} - ${fecha}`;

const ZoomImage = ({ src }: { src: string }) => {
  const [bgPosition, setBgPosition] = useState("center");
  const [isZoomed, setIsZoomed] = useState(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    const { left, top, width, height } = e.currentTarget.getBoundingClientRect();
    const x = ((e.pageX - left) / width) * 100;
    const y = ((e.pageY - top) / height) * 100;
    setBgPosition(`${x}% ${y}%`);
    setIsZoomed(true);
  };

  const handleMouseLeave = () => {
    setBgPosition("center");
    setIsZoomed(false);
  };

  return (
    <div
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      style={{
        width: "100%",
        height: "500px",
        backgroundImage: `url(${src})`,
        backgroundSize: isZoomed ? "200%" : "cover", // o "cover" si prefieres sin márgenes
        backgroundPosition: bgPosition,
        backgroundRepeat: "no-repeat",
        backgroundColor: "#fff", // 👈 Esto elimina el negro
        borderRadius: "12px",
        cursor: "zoom-in",
        border: "1px solid #ccc",
        transition: "background-size 0.3s ease, background-position 0.3s ease",
      }}
    />
  );
};



const TaskResults = ({ taskResult, image }: TaskResultsProps) => {
  const [showClone, setShowClone] = useState(false);
  const cloneRef = useRef<HTMLDivElement>(null);

  const [imageDimensions, setImageDimensions] = useState({ width: 0, height: 0 });
  useEffect(() => {
    const img = new Image();
    img.onload = () => {
      setImageDimensions({ width: img.width, height: img.height });
    };
    img.src = URL.createObjectURL(image);
  }, [image]);

  const fileName = image.name;
  const fileSizeMB = (image.size / 1024 / 1024).toFixed(2); 
  const generatePDF = () => {
    setShowClone(true);

    setTimeout(() => {
      const pdfElement = cloneRef.current;
      if (!pdfElement) return;

      html2canvas(pdfElement, { scale: 2, useCORS: true }).then((canvas) => {
        const imgData = canvas.toDataURL("image/png");
        const pdf = new jsPDF("p", "pt", "a4");
        const imgProps = pdf.getImageProperties(imgData);
        const pdfWidth = pdf.internal.pageSize.getWidth();
        const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
        pdf.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
        pdf.save("informe_vehiclar.pdf");
        setShowClone(false);
      });
    }, 300);
  };

  return (
    <TaskResultsWrapper>
      <div className="laptop">
        <div className="header-bar">
          <div>
            <span className="dot" style={{ background: "#ED594A" }}></span>
            <span className="dot" style={{ background: "#FDD800" }}></span>
            <span className="dot" style={{ background: "#5AC05A" }}></span>
          </div>
         <input
            type="text"
            value="VEHICLAR"
            readOnly
            style={{ background: "transparent", paddingLeft:"100px", border: "none", fontWeight: "600", fontSize: "14px" }}
          />
          <button
            onClick={generatePDF}
            className="download-button"
            title="Descargar PDF"
            style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "6px" }}
          >
            <FaFilePdfIcon size={20} />
          </button>
        </div>

        <div className="content">
          <div className="content-inner">
            <h1 style={{ textAlign: "center", fontSize: "24px", fontWeight: 600, color: "#111827" }}>{HEADER_TEXT}</h1>
            <div className="uploaded-image-wrapper">
              <ZoomImage src={URL.createObjectURL(image)} />
            </div>
            <h1 style={{ textAlign:"center", fontSize: "24px" }}> <strong>RESULTADOS</strong> </h1>
            <div className="result-grid">
              <div className="result-label"><strong>Modelo:</strong></div>
              <div className="result-value">{taskResult["Modelo"]}</div>
              <div className="result-label"><strong>Etiqueta:</strong> </div>
              <div className="result-value">{taskResult["Etiqueta"]}</div>

              <div className="result-label"><strong>Probabilidad:</strong> </div>
              <div className="result-value">{taskResult.Probabilidad}</div>

              <div className="result-label"><strong>Top 3 resultados:</strong> </div>
              <div className="result-value">
                {taskResult["Top 3 resultados"] &&
                  Object.entries(taskResult["Top 3 resultados"]).map(([etiqueta, score]) => (
                    <div key={etiqueta}>{etiqueta}: {(score as number * 100).toFixed(1)}%</div>
                  ))}
              </div>
              <div className="result-label"><strong>Confianza del modelo:</strong></div>
              <div className="result-value">{taskResult["Confianza del modelo"]}</div>
              <div className="result-label"><strong>Nombre del archivo:</strong></div>
              <div className="result-value">{fileName}</div>

              <div className="result-label"><strong>Tamaño:</strong></div>
              <div className="result-value">{fileSizeMB} MB</div>

              <div className="result-label"><strong>Resolución:</strong></div>
              <div className="result-value">
                {imageDimensions.width} x {imageDimensions.height} px
              </div>
              <div className="result-label"><strong>Fecha y Hora:</strong> </div>
              <div className="result-value">{clasificadoEn}</div>
              <div className="result-label"><strong>Resumen:</strong> </div>
              <div
                className="result-value"
                dangerouslySetInnerHTML={{ __html: taskResult.Resumen }}
              />
              

            </div> 

            {!showClone && (
              <p style={{ textAlign: "center", marginTop: "30px", color: "black"}}>
                Si estás conforme con esta clasificación, presiona el botón “<strong>Confirmar</strong>”. Si detectas algún error ajusta la clase manualmente.
              </p>
            )}
          </div>
        </div>
      </div>

      {showClone && (
        <div
          ref={cloneRef}
          style={{
            position: "absolute",
            top: "-10000px",
            left: "-10000px",
            width: "900px",
            padding: "40px",
            background: "#fff",
            fontFamily: "Inter, sans-serif",
            zIndex: -1,
          }}
        >
          <h1 style={{ textAlign: "center", fontSize: "24px", fontWeight: 600 }}>{HEADER_TEXT}</h1>
          <div style={{ maxWidth: "600px", margin: "40px auto", borderRadius: "12px" }}>
          <img src={URL.createObjectURL(image)} alt="uploaded" className="uploaded-image" />
          </div>
          <h1 style={{ textAlign:"center", fontSize: "24px" }}> RESULTADOS </h1>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 2fr",
              gap: "16px",
              maxWidth: "570px",
              margin: "auto",
              padding: "24px",
              background: "#f9fafb",
              borderRadius: "12px",
              border:"1px solid",
            }}
          >
            <div className="result-label"><strong>Modelo:</strong> </div>
            <div className="result-value">{taskResult["Modelo"]}</div>
            <div className="result-label"><strong>Etiqueta:</strong> </div>
              <div className="result-value">{taskResult["Etiqueta"]}</div>

              <div className="result-label"><strong>Probabilidad:</strong> </div>
              <div className="result-value">{taskResult.Probabilidad}</div>

              <div className="result-label"><strong>Top 3 resultados:</strong> </div>
              <div className="result-value">
                {taskResult["Top 3 resultados"] &&
                  Object.entries(taskResult["Top 3 resultados"]).map(([label, score]) => (
                    <div key={label}>{label}: {(score as number * 100).toFixed(2)}%</div>
                  ))}
              </div>
              <div className="result-label"><strong>Confianza del modelo:</strong></div>
              <div className="result-value">{taskResult["Confianza del modelo"]}</div>
              <div className="result-label"><strong>Nombre del archivo:</strong></div>
              <div className="result-value">{fileName}</div>

              <div className="result-label"><strong>Tamaño:</strong></div>
              <div className="result-value">{fileSizeMB} MB</div>

              <div className="result-label"><strong>Resolución:</strong></div>
              <div className="result-value">
                {imageDimensions.width} x {imageDimensions.height} px
              </div>
              <div className="result-label"><strong>Fecha y Hora:</strong> </div>
              <div className="result-value">{clasificadoEn}</div>
              <div className="result-label"><strong>Resumen:</strong> </div>
              <div
                className="result-value"
                dangerouslySetInnerHTML={{ __html: taskResult.Resumen }}
              />
              
          </div>
        </div>
      )}
    </TaskResultsWrapper>
  );
};


export default TaskResults;