import React, { useEffect } from "react";
import styled from "styled-components";

import FancyLoader from "./FancyLoader";
import { fetchCheckStatus } from "../connectors";

type StatusCheckerProps = {
  taskId: string;
  onReady: (isSuccess: boolean, data: unknown) => void;
};

const StatusCheckerWrapper = styled.div`
  transform: scale(1.5);
`;

const StatusChecker = ({ taskId, onReady }: StatusCheckerProps) => {
  useEffect(() => {
    const checkStatus = async () => {
      const data = await fetchCheckStatus(taskId);

      if (data?.status === "Pending") {
        setTimeout(() => {
          checkStatus();
        }, 3000);
      } else {
        onReady(data?.status === "Success", data?.response);
      }
    };

    checkStatus();
  }, [taskId, onReady]);

  return (
    <StatusCheckerWrapper>
      <FancyLoader />
    </StatusCheckerWrapper>
  );
};

export default StatusChecker;
