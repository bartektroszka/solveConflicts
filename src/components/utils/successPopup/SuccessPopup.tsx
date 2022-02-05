import { Props } from './types';
import { $SuccessPopup } from './SuccessPopup.style';
import { useEffect, useState } from 'react';
import { $Notification } from './SuccessPopup.style';
const SuccessPopup = ({ width, height, completed }: Props) => {
  const [open, setOpen] = useState(true);

  useEffect(() => {
    setInterval(() => {
      setOpen(false);
      completed();
    }, 3000);
  }, [completed]);
  return open ? (
    <$SuccessPopup>
      <$Notification width={width} height={height}>
        <img width='150px' height='150px' src='success.svg' alt='success'></img>
        Przeszedłeś Poziom!
      </$Notification>
    </$SuccessPopup>
  ) : null;
};

export default SuccessPopup;
