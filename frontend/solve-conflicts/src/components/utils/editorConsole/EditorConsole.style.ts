import { ContainerProps } from './types';
import styled from 'styled-components';

export const $EditorConsoleContainer = styled.div`
  height: 100%;
  display: flex;
  gap: 0.5rem;
  flex-direction: row-reverse;
  background-color: grey;
`;

export const $ConsoleContainer = styled.div`
  width: 30%;
  height: 100%;
  div.sc-EHOje.dMFuoo {
    overflow: hidden !important;
  }
  .gSZAyM {
    min-height: 0px !important;
  }
  display: flex;
`;

export const $AllContainer = styled.div<ContainerProps>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  background-color: grey;
  display: flex;
  flex-direction: column;
  padding: 0.5rem;
`;

export const $BottomLine = styled.div`
  display: flex;
  width: 100%;
  justify-content: flex-end;
  align-items: center;
  button {
    margin-top: 0.5rem;
  }
`;
