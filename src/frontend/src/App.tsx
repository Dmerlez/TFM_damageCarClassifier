import React, { useCallback, useState } from "react";
import styled from "styled-components";

import ActionButtons from "./components/ActionButtons";
import FileUpload from "./components/FileUpload";
import StatusChecker from "./components/StatusChecker";
import Robot from "./components/Robot";
import TaskResults from "./components/TaskResults";
import {
  ERROR_ALERT_TEXT,
  ROBOT_TEXT_FINAL,
  ROBOT_TEXT_INITIAL,
  ROBOT_TEXT_PENDING,
} from "./constants/texts";

import "./App.css";

const StyledWrapper = styled.div`
  height: 100vh;

  .dropzone-container {
    max-width: 50%;
    margin: 500px auto;
    z-index: 100;
  }

  .status-checker-container {
    margin: 350px auto;
    z-index: 100;
  }

  .final-result-container {
    width: 100%;
    margin: 50px 50px 100px 500px;
    z-index: 100;
  }
`;

function App() {
  const [taskResponse, setTaskResponse] = useState<unknown>();
  const [taskId, setTaskId] = useState<string>();
  const [uploadedImage, setUploadedImage] = useState<File>();

  const handleFileUploadSuccess = (createdTaskId: string, image: File) => {
    setTaskId(createdTaskId);
    setUploadedImage(image);
  };

  const handleTaskReady = useCallback((isSuccess: boolean, data: unknown) => {
    if (isSuccess) {
      setTaskResponse(data);
    } else {
      alert(ERROR_ALERT_TEXT);
      window.location.reload();
    }
  }, []);

  const renderContent = () => {
    if (taskResponse) {
      return (
        <div className="final-result-container">
          <Robot
            direction="bottom"
            position={{ left: "230px", top: "280px" }}
            text={ROBOT_TEXT_FINAL}
            actions={<ActionButtons />}
          />
          <TaskResults taskResult={taskResponse} image={uploadedImage!} />
        </div>
      );
    }

    if (taskId) {
      return (
        <div className="status-checker-container">
          <Robot
            direction="left"
            position={{ left: "75%", top: "300px" }}
            text={ROBOT_TEXT_PENDING}
          />
          <StatusChecker taskId={taskId} onReady={handleTaskReady} />
        </div>
      );
    }

    return (
      <>
        <Robot
          position={{ left: "25%", top: "300px" }}
          text={ROBOT_TEXT_INITIAL}
        />
        <div className="dropzone-container">
          <FileUpload onSuccess={handleFileUploadSuccess} />
        </div>
      </>
    );
  };

  return <StyledWrapper className="App">{renderContent()}</StyledWrapper>;
}

export default App;
