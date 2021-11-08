import { Props } from './types';
import { $Popup, $Notification, $ButtonContainer } from './Popup.style';
import { Button } from '../button/Button';
const Popup = ({ width, height, children, open, setOpen }: Props) => {
  return open ? (
    <$Popup>
      <$Notification width={width} height={height}>
        {children}

        <$ButtonContainer>
          <Button buttonText='CLOSE' onClick={() => setOpen(!open)}></Button>
        </$ButtonContainer>
      </$Notification>
    </$Popup>
  ) : null;
};

export default Popup;
