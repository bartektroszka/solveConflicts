import { buttonRadius } from "src/constants";
import styled from "styled-components";

export const $Popup = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
`;
export const $DiplomaChildren = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  justify-content: center;
`;

export const $DiplomaInput = styled.input`
  width: 250px;
  height: 40px;
  border-radius: 10px;
  padding: 0.2em 0.5em;
  outline: none;
  white-space: nowrap;
  -webkit-user-select: none;
  cursor: pointer;
  text-shadow: 1px 1px #fff;
  background: linear-gradient(top, #f9f9f9, #e3e3e3);
  border: 1px solid #999;
  font-weight: 500;
  font-size: 20px;
  display: flex;
  justify-content: center;
`;
export const $Notification = styled.div<{ width: string; height: string }>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  z-index: 10;
  background-color: rgba(170, 170, 170);
  border-radius: ${buttonRadius};
  box-shadow: 4px 2px 2px black;
  font-size: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 15px;
  padding-left: 30px;
  padding-right: 30px;
  top: 0px;
  animation: drop 0.7s ease forwards;
  @keyframes drop {
    0% {
      opacity: 0;
    }
    70% {
      transform: translateY(30%);
    }
    100% {
      transform: translateY(0%);
      opacity: 1;
    }
  }
`;

export const $ChildrenContainer = styled.div`
  display: flex;
  justify-content: center;
  height: 100%;
  align-items: center;
`;
export const $ButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  gap: 1rem;
`;
