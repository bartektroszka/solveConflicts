import { buttonRadius, secondaryColor } from 'src/constants';
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
