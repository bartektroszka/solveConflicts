import { ContainerProps } from './types';
import styled from 'styled-components';
import { backgroundColor } from 'src/constants';

export const $EditorConsoleContainer = styled.div`
  height: 100%;
  display: flex;
  width: 95%;
  gap: 0.5rem;
  flex-direction: row-reverse;
  background-color: ${backgroundColor};
`;

export const $ConsoleContainer = styled.div`
  height: 100%;
  max-height: 100%;
  flex-basis: 45%;
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
  max-height: ${(props) => props.height};
  flex-grow: 0;
  height: ${(props) => props.height};
  background-color: ${backgroundColor};
  display: flex;
  flex-direction: column;
  padding: 0.5rem;
`;

export const $EditorContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 90%;
  height: 100%;
`;

export const $GitTreeContainer = styled.div`
  display: flex;
  width: 25%;
  flex-direction: column;
  gap: 2rem;
  transform: scale(0.8);
`;

export const $ButtonsContainer = styled.div`
  height: 1.8rem;
  display: flex;
  width: 100%;
  justify-content: flex-end;
  gap: 1rem;
  position: absolute;
  right: 0.5rem;
`;

export const $EmptyLine = styled.div`
  height: 2rem;
`;
export const $BottomLine = styled.div`
  display: flex;
  width: 100%;
  justify-content: flex-end;
  height: 0px;
  align-items: center;
  button {
    position: relative;
    bottom: 32px;
    right: 14px;
    z-index: 7;
  }
`;
