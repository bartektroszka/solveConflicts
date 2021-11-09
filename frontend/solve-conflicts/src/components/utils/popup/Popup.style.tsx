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
  border-radius: 10px;
  box-shadow: 4px 2px 2px black;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 15px;
`;

export const $ButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
`;
