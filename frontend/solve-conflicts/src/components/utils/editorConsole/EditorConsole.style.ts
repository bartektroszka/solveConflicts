import { ContainerProps } from './types';
import styled from 'styled-components';
import { backgroundColor } from 'src/constants';

export const $EditorConsoleContainer = styled.div`
  height: 100%;
  display: flex;
  width: 100%;
  gap: 0.5rem;
  flex-direction: row-reverse;
  background-color: ${backgroundColor};
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
  background-color: ${backgroundColor};
  display: flex;
  flex-direction: column;
  padding: 0.5rem;
`;

export const $EditorContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
`;

export const $GitTreeContainer = styled.div`
  display: flex;
  width: 30%;
`;

export const $BottomLine = styled.div`
  display: flex;
  width: 100%;
  justify-content: flex-end;
  height: 0px;
  align-items: center;
  button {
    position: relative;
    bottom: 25px;
    right: 7px;
  }
`;
