import React from "react";
import styled from "styled-components";

const ActionButtonsWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  width: 400px;
  position: absolute;
  left: -10px;
  bottom: -120px;

  button {
    margin: 20px 20px 20px 0;
    padding: 20px 50px;
    position: relative;
    font-size: 20px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    background: #000;
    cursor: pointer;
    z-index: 0;
    transition: 0.5s;
  }
  button:first-child {
    border: 2px solid #43ea0f;
    color: #43ea0f;
    box-shadow: 0 0 20px 0 #43ea0f;
  }
  button:nth-child(2) {
    border: 2px solid #ea0fea;
    color: #ea0fea;
    box-shadow: 0 0 20px 0 #ea0fea;
  }
  button:last-child {
    border: 2px solid #ff531a;
    color: #ff531a;
    box-shadow: 0 0 20px 0 #ff531a;
  }
  button::before {
    content: "";
    position: absolute;
    top: -5px;
    left: -5px;
    width: 10px;
    height: 10px;
    background: #000;
    z-index: -1;
    border-radius: 50%;
    transition: 0.5s;
  }
  button:first-child::before {
    border: 2px solid #43ea0f;
  }
  button:nth-child(2)::before {
    border: 2px solid #ea0fea;
  }
  button:last-child::before {
    border: 2px solid #ff531a;
  }
  button::after {
    content: "";
    position: absolute;
    bottom: -5px;
    right: -5px;
    width: 10px;
    height: 10px;
    background: #000;
    z-index: -1;
    border-radius: 50%;
    transition: 0.5s;
  }
  button:first-child::after {
    border: 2px solid #43ea0f;
  }
  button:nth-child(2)::after {
    border: 2px solid #ea0fea;
  }
  button:last-child::after {
    border: 2px solid #ff531a;
  }
  button:hover::before {
    left: calc(100% - 5px);
  }
  button:hover::after {
    right: calc(100% - 5px);
  }
  button:first-child:hover {
    color: #000;
    background: #43ea0f;
    box-shadow: 0 0 60px 0 #43ea0f;
  }
  button:nth-child(2):hover {
    color: #000;
    background: #ea0fea;
    box-shadow: 0 0 60px 0 #ea0fea;
  }
  button:last-child:hover {
    color: #000;
    background: #ff531a;
    box-shadow: 0 0 60px 0 #ff531a;
  }
`;

const ActionButtons = () => {
  const handleOkClick = () => {
    alert("Your data was successfully transferred!");
    window.location.reload();
  };

  const handleCancelClick = () => window.location.reload();

  return (
    <ActionButtonsWrapper>
      <button onClick={handleOkClick} className="ok-button">
        Confirm
      </button>
      <button onClick={handleCancelClick} className="cancel-button">
        Cancel
      </button>
    </ActionButtonsWrapper>
  );
};

export default ActionButtons;
