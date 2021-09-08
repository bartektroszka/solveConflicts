import { ContainerProps } from "./types";
import styled from "styled-components";

export const $EditorConsoleContainer = styled.div<ContainerProps>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  padding: 0.5rem;
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
  display: flex;
`;
