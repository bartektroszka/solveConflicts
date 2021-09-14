import { Props } from "./types";
import { $Popup, $Notification } from "./Popup.style";
const Popup = ({ width, height, children, open }: Props) => {
  return (
    <$Popup>
      {open ? (
        <$Notification width={width} height={height}>
          {children}
        </$Notification>
      ) : null}
    </$Popup>
  );
};

export default Popup;
