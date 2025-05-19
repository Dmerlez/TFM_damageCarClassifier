import React from "react";
import styled from "styled-components";

type TaskResultsProps = any; // { taskResult: unknown }; PS: fucking TS

const TaskResultsWrapper = styled.div`
  width: inherit;
  position: relative;

  .laptop {
    -webkit-transform-origin: 0 0;
    transform-origin: 0 0;
    -webkit-transform: scale(0.8) translate(-50%);
    transform: scale(0.8) translate(-50%);
    left: 50%;
    position: absolute;
    width: 100%;
    height: 75vh;
    border-radius: 6px;
    border-style: solid;
    border-color: rgb(70, 70, 70);
    border-width: 24px 24px 60px;
    background-color: rgb(70, 70, 70);
  }

  /* The keyboard of the laptop */
  .laptop:after {
    content: "";
    display: block;
    position: absolute;
    width: calc(100% + 220px);
    height: 60px;
    margin: 60px 0 0 -110px;
    background: rgb(70, 70, 70);
    border-radius: 6px;
    border: solid rgb(60, 60, 60);
    border-width: 5px 0px 0px;
    box-shadow: 0px -5px 10px rgb(60, 60, 60);
  }

  /* The top of the keyboard */
  .laptop:before {
    content: "";
    display: block;
    position: absolute;
    width: 250px;
    height: 30px;
    bottom: -95px;
    left: 50%;
    -webkit-transform: translate(-50%);
    transform: translate(-50%);
    background: gray;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    z-index: 1;
  }

  /* The screen (or content) of the device */
  .laptop .content {
    background-color: white;
    height: 100%;
    width: 100%;
    border-radius: 10px;
    font-size: 16px;
    box-sizing: border-box;
    overflow: scroll;

    .container {
      border-top-left-radius: 4px;
      border-top-right-radius: 4px;
    }

    .header {
      position: sticky;
      top: 0;
    }

    /* Container for columns and the top "toolbar" */
    .row {
      padding: 10px;
      background: #f1f1f1;
      border-top-left-radius: 4px;
      border-top-right-radius: 4px;
    }

    /* Create three unequal columns that floats next to each other */
    .column {
      float: left;
    }

    .left {
      width: 15%;
    }

    .right {
      width: 10%;
    }

    .middle {
      width: 75%;
    }

    .row:after {
      content: "";
      display: table;
      clear: both;
    }

    .dot {
      margin-top: 5px;
      margin-right: 5px;
      height: 12px;
      width: 12px;
      background-color: #bbb;
      border-radius: 50%;
      display: inline-block;
    }

    input[type="text"] {
      width: 100%;
      border-radius: 3px;
      border: none;
      background-color: white;
      margin-top: -8px;
      height: 25px;
      color: #666;
      padding: 5px;
    }

    .bar {
      width: 17px;
      height: 3px;
      background-color: #aaa;
      margin: 3px 0;
      display: block;
    }
  }

  .content-inner {
    padding: 25px;
    font-size: 22px;

    .uploaded-image {
      display: flex;
      width: 50%;
      margin: auto;
      box-shadow: 0px 0px 15px lightgray;
    }

    .task-result {
      .section {
        .title {
          text-transform: capitalize;
        }
        .value {
          margin-left: 20px;
        }
      }
    }
  }
`;

const HEADER_TEXT =
  "Hemos analizado la imagen y obtenido los siguientes resultados: ";

const FOOTER_TEXT =
  "Si estás conforme con este classificación, presiona el botón “Confirmar”. Si detectas algún error ajusta la clase manualmente.";

const renderStructuredTaskResults = (
  taskResult: TaskResultsProps
): React.JSX.Element => {
  const sections = Object.keys(taskResult);

  return (
    <div className="task-result">
      {sections.map((section) => (
        <div className="section" key={section}>
          <h3 className="title">{section}</h3>
          <p className="value">{taskResult[section]}</p>
        </div>
      ))}
    </div>
  );
};

const TaskResults = ({ taskResult, image }: TaskResultsProps) => (
  <TaskResultsWrapper>
    <div className="laptop">
      <div className="content">
        <div className="container">
          <div className="header row">
            <div className="column left">
              <span className="dot" style={{ background: "#ED594A" }}></span>
              <span className="dot" style={{ background: "#FDD800" }}></span>
              <span className="dot" style={{ background: "#5AC05A" }}></span>
            </div>
            <div className="column middle">
              <input
                type="text"
                value="https://www.somia.com/sabentis/onboarding/assist"
              />
            </div>
            <div className="column right">
              <div style={{ float: "right" }}>
                <span className="bar"></span>
                <span className="bar"></span>
                <span className="bar"></span>
              </div>
            </div>
          </div>

          <div className="content-inner">
            <p className="header-text">{HEADER_TEXT}</p>
            <img
              src={URL.createObjectURL(image)}
              alt="uploaded-image"
              className="uploaded-image"
            />
            {renderStructuredTaskResults(taskResult)}
            <p className="footer-text">{FOOTER_TEXT}</p>
          </div>
        </div>
      </div>
    </div>
  </TaskResultsWrapper>
);

export default TaskResults;
