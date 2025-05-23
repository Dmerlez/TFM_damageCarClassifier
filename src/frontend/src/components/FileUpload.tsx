import React from "react";
import { useDropzone } from "react-dropzone";
import styled from "styled-components";
import { SlCloudUpload } from "react-icons/sl";

import { fetchUpload } from "../connectors";

const SlCloudUploadCasted = SlCloudUpload as any; // fucking TS 🤦‍♂️

type FileUploadProps = {
  onSuccess: (id: string, image: File) => void;
};

const StyledWrapper = styled.div`
  display: block;

  background-color: rgba(6, 3, 21, 0.6);
  border: 2px dashed gray;
  border-radius: 10px;

  z-index: 100;

  /* 👇 Ajuste de posición vertical */
  margin-top: -250px; /* Puedes probar también -40px o -50px según lo necesites */

  .dropzone {
    cursor: pointer;
    width: 100%;
    height: 100%;
    display: flex;
    text-align: center;
    padding: 30px;
    box-sizing: border-box;
    flex-direction: column;
    align-items: center;
    color: white;
    font-family: monospace;

    &:hover {
      text-shadow: 1px 1px 10px;
      transition: text-shadow 1s;

      .upload-icon {
        transform: scale(1.1);
        transition: transform 1s;
      }
    }

    .upload-message {
      margin: 0;
      font-size: 25px;
    }

    .upload-icon {
      font-size: 100px;
      margin-top: 25px;
    }
  }
`;


const FileUpload = ({ onSuccess }: FileUploadProps) => {
  const onDrop = async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];

    const formData = new FormData();
    formData.append("file", file);

    const createdTaskId = await fetchUpload(formData);
    if (createdTaskId) {
      onSuccess(createdTaskId, file);
    }
  };

  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept: {
        "image/*": [],
        },
    multiple: false,
  });


  return (
    <StyledWrapper>
      <div {...getRootProps()} className="dropzone">
        <input {...getInputProps()} />
        <p className="upload-message">ARRASTRA O SUBE LA IMAGEN DE TU AUTO</p>
        <SlCloudUploadCasted className="upload-icon" />
      </div>
    </StyledWrapper>
  );
};

export default FileUpload;
