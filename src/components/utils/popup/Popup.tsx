import { Props } from './types';
import {
  $Popup,
  $Notification,
  $ButtonContainer,
  $ChildrenContainer,
} from './Popup.style';
import { Button } from '../button/Button';
import { useEffect, useRef } from 'react';
const Popup = ({
  width,
  height,
  children,
  open,
  afterClose,
  buttonText,
}: Props) => {

  const handleKeypress = (e:any) => {
    if (e.keyCode === 13) {
      afterClose()    }
  };
 
  const mainRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    mainRef.current?.focus();
  }) 
  
  return open ? (
    <$Popup ref={mainRef}
            onKeyDown={handleKeypress}
            tabIndex={-1}>
      <$Notification width={width} height={height}>
        <$ChildrenContainer>{children}</$ChildrenContainer>
        <$ButtonContainer>
          <Button buttonText={buttonText} onClick={afterClose}></Button>
        </$ButtonContainer>
      </$Notification>
    </$Popup>
  ) : null;
};

export default Popup;
