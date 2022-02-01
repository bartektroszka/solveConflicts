import { buttonRadius, secondaryColor, secondaryDarkColor } from 'src/constants';
import styled from 'styled-components';
import { Size } from '../../../types';

export const $Button = styled.button<Size>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  cursor: pointer;
  background-color: ${secondaryColor};
  border: none;
  font-size: 0.9rem;
  border-radius: ${buttonRadius};
`;

export const $LoadingButton= styled.button<Size>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  background-color: #4db8ff;
  border: none;
  font-size: 0.9rem;
  border-radius: ${buttonRadius};
`;