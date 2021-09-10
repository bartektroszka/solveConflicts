import styled from "styled-components";
import { Size } from "./types";

export const $LevelBar = styled.div<Size>`
  display: flex;
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  border: 1px solid #000;
  justify-content: center;
`;

const $Level = styled.div<Size>`
  width: 100%;
  height: ${(props) => props.height};
  border-right: 1px solid #000;
  font-weight: 400;
  font-size: 75px;
  color: rgb(180, 180, 180);
  text-align: center;
`;
export const $CompletedLevel = styled($Level)<Size>`
  background: linear-gradient(
    102deg,
    rgba(40, 139, 18, 1) 0%,
    rgba(70, 184, 37, 1) 58%,
    rgba(96, 203, 67, 1) 90%,
    rgba(90, 222, 77, 1) 100%
  );
`;

export const $CurrentLevel = styled($Level)<Size>`
  background: linear-gradient(
    90deg,
    rgba(28, 62, 119, 1) 0%,
    rgba(47, 122, 177, 1) 58%,
    rgba(88, 140, 240, 1) 90%,
    rgba(44, 138, 190, 1) 100%
  );
`;

export const $FutureLevel = styled($Level)<Size>`
  background: linear-gradient(
    102deg,
    rgba(84, 84, 84, 1) 0%,
    rgba(119, 119, 119, 1) 58%,
    rgba(157, 157, 157, 1) 90%,
    rgba(191, 191, 191, 1) 100%
  );
`;
