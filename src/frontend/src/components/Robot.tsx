import React from "react";
import styled from "styled-components";
import SpeechBubble from "./SpeechBubble";
import SVG from "react-inlinesvg";

import robot from "../robot.svg";

const InlineSVG = SVG as any;

type Direction = "left" | "right" | "top" | "bottom";

type Position = { left: string; top: string };

export type RobotProps = {
  actions?: React.JSX.Element;
  position: Position;
  direction?: Direction;
  text: React.JSX.Element | string;
  showSpeech?: boolean;
};

type RobotWrapperProps = { $position: Position; $direction?: Direction };

const RobotWrapper = styled.div<RobotWrapperProps>`
  z-index: 90;

  .robot svg {
    position: absolute;
    top: ${({ $position }) => $position.top};
    left: ${({ $position }) => $position.left};
    display: block;
    margin: 0 auto;
    display:none;
    transform: scale(0.6) translate(0, -100%);
    transform-origin: center;
    height: 800px;
    width: 600px;
  }

  .credit {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    color: rgba(255, 255, 255, 0.3);
  }

  .credit a {
    color: rgba(255, 255, 255, 0.6);
  }
`;

const Robot = ({
  position,
  direction = "right",
  text,
  actions,
  showSpeech = true, // 👈 por defecto sí se muestra
}: RobotProps) => (
  <RobotWrapper $position={position} $direction={direction}>
    <div className="robot">
      <InlineSVG src={robot} />
    </div>
    {showSpeech && (
      <SpeechBubble
        position={position}
        direction={direction}
        text={text}
        actions={actions}
      />
    )}
  </RobotWrapper>
);

export default Robot;
