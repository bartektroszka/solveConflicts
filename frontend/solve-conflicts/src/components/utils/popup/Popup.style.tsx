import { buttonRadius } from 'src/constants';
import styled from 'styled-components';

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
`;
