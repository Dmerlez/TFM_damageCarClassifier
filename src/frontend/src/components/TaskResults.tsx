import React, { useState, useRef } from "react";
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
  font-family: 'Inter', sans-serif;
  padding: 40px 20px;

  .laptop {
    position: relative;
    max-width: 900px;
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
    background: #e5e7eb;
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
    background-color: white;
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
    max-width: 500px;
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
    max-width: 450px;
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

const HEADER_TEXT = "Imagen analizada:";
const FOOTER_TEXT = "Si estás conforme con esta clasificación, presiona el botón “Confirmar”. Si detectas algún error ajusta la clase manualmente.";

const TaskResults = ({ taskResult, image }: TaskResultsProps) => {
  const [showClone, setShowClone] = useState(false);
  const cloneRef = useRef<HTMLDivElement>(null);

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
          <center><input
            type="text"
            value="VEHICLAR"
            readOnly
            style={{ background: "transparent", border: "none", fontWeight: "600", fontSize: "14px" }}
          />
          </center>
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
              <img src={URL.createObjectURL(image)} alt="uploaded" className="uploaded-image" />
            </div>
            <h1 style={{ textAlign:"center", fontSize: "24px" }}> Resultados CLIP + MLPClassifier</h1>
            <div className="result-grid">
              <div className="result-label">Label: </div>
              <div className="result-value">{taskResult["Label"]}</div>

              <div className="result-label">Probability: </div>
              <div className="result-value">{taskResult.Probability}</div>

              <div className="result-label">Top 3 scores: </div>
              <div className="result-value">
                {taskResult["Top 3 scores"] &&
                  Object.entries(taskResult["Top 3 scores"]).map(([label, score]) => (
                    <div key={label}>{label}: {(score as number * 100).toFixed(2)}%</div>
                  ))}
              </div>

              <div className="result-label">Final result: </div>
              <div className="result-value">{taskResult["Final result"]}</div>
            </div> 

            {!showClone && (
              <p style={{ textAlign: "center", marginTop: "30px", color: "#6b7280" }}>
                {FOOTER_TEXT}
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
          <h1 style={{ textAlign:"center", fontSize: "24px" }}> Resultados CLIP + MLPClassifier</h1>
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
            
            <div className="result-label">Label: </div>
              <div className="result-value">{taskResult["Label"]}</div>

              <div className="result-label">Probability: </div>
              <div className="result-value">{taskResult.Probability}</div>

              <div className="result-label">Top 3 scores: </div>
              <div className="result-value">
                {taskResult["Top 3 scores"] &&
                  Object.entries(taskResult["Top 3 scores"]).map(([label, score]) => (
                    <div key={label}>{label}: {(score as number * 100).toFixed(2)}%</div>
                  ))}
              </div>

              <div className="result-label">Final result: </div>
              <div className="result-value">{taskResult["Final result"]}</div>
          </div>
        </div>
      )}
    </TaskResultsWrapper>
  );
};

export default TaskResults;