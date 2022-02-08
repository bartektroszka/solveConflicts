import {
  buttonRadius,
  buttonTextColor,
  buttonTextSize,
  buttonTextWeight,
  disabledGrey,
  disabledGreyTexts,
  secondaryColor,
  secondaryDarkColor,
} from 'src/constants';
import styled from 'styled-components';
import { Size } from '../../../types';

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
  border-radius: ${buttonRadius};
  :hover {
    transform: scale(1.05);
  }
  font-size: ${buttonTextSize};
  color: ${buttonTextColor};
  font-weight: ${buttonTextWeight};
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
  border-radius: ${buttonRadius};
  color: ${disabledGreyTexts};
  font-size: ${buttonTextSize};
  font-weight: ${buttonTextWeight};
`;
