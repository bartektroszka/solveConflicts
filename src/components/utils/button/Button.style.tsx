import styled from 'styled-components';
import { Size } from '../../../types';

export const $Button = styled.button<Size>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  cursor: pointer;
  background-color: #179af1;
  border: none;
  border-radius: 5px;
  
`;
