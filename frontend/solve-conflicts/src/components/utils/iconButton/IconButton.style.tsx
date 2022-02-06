import {
  buttonRadius,
  disabledGrey,
  disabledGreyTexts,
  secondaryColor,
  secondaryDarkColor,
} from "src/constants";
import styled from "styled-components";
import { Size } from "../../../types";

export const $IconButton = styled.button<Size>`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  cursor: pointer;
  background-color: ${secondaryColor};
  border: none;
  font-size: 0.9rem;
  border-radius: ${buttonRadius};
  :hover {
    transform: scale(1.05);
  }
`;

export const $IconButtonDisabled = styled.button<Size>`
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  background-color: ${disabledGrey};
  border: none;
  font-size: 0.9rem;
  border-radius: ${buttonRadius};
  color: ${disabledGreyTexts};
`;
