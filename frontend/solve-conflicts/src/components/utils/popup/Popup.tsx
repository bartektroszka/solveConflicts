import { Props } from './types';
import { $Popup, $Notification, $ButtonContainer } from './Popup.style';
import { Button } from '../button/Button';
const Popup = ({
  width,
  height,
  children,
  open,
  afterClose,
  buttonText,
}: Props) => {
  return open ? (
    <$Popup>
      <$Notification width={width} height={height}>
        {children}
        <$ButtonContainer>
          <Button buttonText={buttonText} onClick={afterClose}></Button>
        </$ButtonContainer>
      </$Notification>
    </$Popup>
  ) : null;
};

export default Popup;
