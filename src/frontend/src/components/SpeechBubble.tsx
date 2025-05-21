import React from "react";
import styled from "styled-components";

import type { RobotProps } from "./Robot";

type SpeechBubbleProps = {
  actions?: RobotProps["actions"];
  direction: RobotProps["direction"];
  position: RobotProps["position"];
  text: RobotProps["text"];
};

type BubbleWrapperProps = {
  $direction: RobotProps["direction"];
  $position: RobotProps["position"];
};

const LEFT_STYLES = `
  height: 4px;
  width: 4px;
  top: 20px;
  left: -8px;
  background: white;
  box-shadow: -4px -4px #fff, -4px 0 #fff, -8px 0 #fff, 0 -8px #fff, -4px 4px #000, -8px 4px #000, -12px 4px #000, -16px 4px #000, -12px 0 #000, -8px -4px #000, -4px -8px #000, 0 -4px #fff;
`;

const RIGHT_STYLES = `
  height: 4px;
  width: 4px;
  top: 84px;
  right: -8px;
  background: white;
  box-shadow: 4px -4px #fff, 4px 0 #fff, 8px 0 #fff, 0 -8px #fff, 4px 4px #000, 8px 4px #000, 12px 4px #000, 16px 4px #000, 12px 0 #000, 8px -4px #000, 4px -8px #000, 0 -4px #fff;
`;

const TOP_STYLES = `
  height: 4px;
  width: 4px;
  top: -8px;
  left: 32px;
  box-shadow: 0 -4px #000, 0 -8px #000, 0 -12px #000, 0 -16px #000, -4px -12px #000, -8px -8px #000, -12px -4px #000, -4px -4px #fff, -8px -4px #fff, -4px -8px #fff, -4px 0 #fff, -8px 0 #fff, -12px 0 #fff;
`;

const BOTTOM_STYLES = `
  height: 4px;
  width: 4px;
  bottom: -8px;
  left: 32px;
  box-shadow: 0 4px #000, 0 8px #000, 0 12px #000, 0 16px #000, -4px 12px #000, -8px 8px #000, -12px 4px #000, -4px 4px #fff, -8px 4px #fff, -4px 8px #fff, -4px 0 #fff, -8px 0 #fff, -12px 0 #fff;
`;

const BubbleWrapper = styled.div<BubbleWrapperProps>`
  position: absolute;

  top: ${({ $direction, $position }) => {
    switch ($direction) {
      case "top":
        return `calc(${$position.top} - 400px)`;
      case "bottom":
        return `calc(${$position.top} + 50px)`;
      case "left":
        return `calc(${$position.top} - 200px)`;
      case "right":
      default:
        return `calc(${$position.top} - 200px)`;
    }
  }};

  left: ${({ $direction, $position }) => {
    switch ($direction) {
      case "top":
        return `calc(${$position.left} - 200px)`;
      case "bottom":
        return `calc(${$position.left} - 200px)`;
      case "left":
        return `calc(${$position.left} - 800px)`;
      case "right":
      default:
        return `calc(${$position.left} + 175px)`;
    }
  }};

  display: inline-block;
  margin: 20px;
  line-height: 1.3em;
  background-color: #fff;
  color: #000;
  padding: 12px;
  box-shadow: 0 -4px #fff, 0 -8px #000, 4px 0 #fff, 4px -4px #000, 8px 0 #000,
    0 4px #fff, 0 8px #000, -4px 0 #fff, -4px 4px #000, -8px 0 #000,
    -4px -4px #000, 4px 4px #000;
  box-sizing: border-box;
  width: ${({ $direction }) => {
    switch ($direction) {
      case "top":
      case "bottom":
        return "400px";
      case "left":
      case "right":
      default:
        return "600px";
    }
  }};
  font-size: 22px;
  text-align: left;
  text-transform: uppercase;
  font-weight: bold;
  box-shadow: 0 -4px #fff, 0 -8px #000, 4px 0 #fff, 4px -4px #000, 8px 0 #000,
    0 4px #fff, 0 8px #000, -4px 0 #fff, -4px 4px #000, -8px 0 #000,
    -4px -4px #000, 4px 4px #000, 4px 12px rgba(0, 0, 0, 0.1),
    12px 4px rgba(0, 0, 0, 0.1), 8px 8px rgba(0, 0, 0, 0.1);

  p {
    margin: 0;
  }

  &::after {
    content: "";
    display: block;
    position: absolute;
    box-sizing: border-box;

    ${({ $direction }) => {
      switch ($direction) {
        case "top":
          return BOTTOM_STYLES;
        case "bottom":
          return TOP_STYLES;
        case "left":
          return RIGHT_STYLES;
        case "right":
        default:
          return LEFT_STYLES;
      }
    }}
  }
`;

const SpeechBubble = ({
  actions,
  direction,
  position,
  text,
}: SpeechBubbleProps) => (
  <BubbleWrapper $direction={direction} $position={position}>
    {text}
    {actions}
  </BubbleWrapper>
);

export default SpeechBubble;
