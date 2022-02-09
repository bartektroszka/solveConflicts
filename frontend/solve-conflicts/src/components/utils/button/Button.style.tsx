import {
  buttonRadius,
  buttonTextColor,
  buttonTextSize,
  buttonTextWeight,
  secondaryBrightColor,
  secondaryBrighterColor,
  secondaryColor,
  secondaryDarkColor,
} from 'src/constants';
import styled from 'styled-components';
import { Size } from '../../../types';

export const $Button = styled.button<Size>`
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

export const $HighlightedButton = styled.button<Size>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  cursor: pointer;
  background-color: ${secondaryBrightColor};
  border: none;
  border-radius: ${buttonRadius};
  :hover {
    transform: scale(1.05);
  }
  font-size: ${buttonTextSize};
  color: ${buttonTextColor};
  font-weight: ${buttonTextWeight};
`;
export const $LoadingButton = styled.button<Size>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  background-color: ${secondaryBrighterColor};
  border: none;
  border-radius: ${buttonRadius};
  font-size: ${buttonTextSize};
  color: ${buttonTextColor};
  font-weight: ${buttonTextWeight};
`;
