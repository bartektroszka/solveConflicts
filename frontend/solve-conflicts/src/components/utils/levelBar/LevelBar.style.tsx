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
  padding: 1rem;
  gap: 1.5rem;
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
  background-color: #81b375;
  cursor: pointer;
  :hover {
    transform: scale(1.05);
  }
`;

export const $CurrentLevel = styled($Level)<Size>`
  background-color: ${secondaryColor};
  cursor: pointer;
  :hover {
    transform: scale(1.05);
  }
`;

export const $AvailableLevel = styled($Level)<Size>`
  background-color: #ffd500;
  cursor: pointer;
  :hover {
    transform: scale(1.05);
  }
`;

export const $FutureLevel = styled($Level)<Size>`
  background-color: ${secondaryDarkColor};
`;
