import {
  buttonRadius,
  secondaryColor,
  secondaryDarkColor,
} from 'src/constants';
import styled from 'styled-components';
import { Size } from '../../../types';

export const $LevelBar = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 1.5rem;
  gap: 2rem;
  flex-shrink: 0;
`;

const $Level = styled.div<Size>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  font-weight: 400;
  font-size: 2rem;
  color: white;
  text-align: center;
  border-radius: ${buttonRadius};
  z-index: 2;
`;

export const $CompletedLevel = styled($Level)<Size>`
  background-color: ${secondaryDarkColor};
`;

export const $CurrentLevel = styled($Level)<Size>`
  background-color: ${secondaryColor};
`;

export const $FutureLevel = styled($Level)<Size>`
  background-color: ${secondaryDarkColor};
`;
