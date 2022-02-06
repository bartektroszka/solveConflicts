import {
  $Popup,
  $Notification,
  $ButtonContainer,
  $ChildrenContainer,
  $DiplomaChildren,
  $DiplomaInput,
} from "./DiplomaPopup.style";
import { Button } from "../button/Button";
import { useEffect, useRef, useState } from "react";
import { Props } from "./types";

const Popup = ({ handleClose, handleSubmit }: Props) => {
  const [name, setName] = useState<string>("");
  return (
    <$Popup>
      <$Notification width={"500px"} height={"200px"}>
        <$ChildrenContainer>
          <$DiplomaChildren>
            <div>Podaj imię i nazwisko, które mają być na dyplomie</div>
            <$DiplomaInput
              value={name}
              onChange={(val) => setName(val.target.value)}
            ></$DiplomaInput>
          </$DiplomaChildren>
        </$ChildrenContainer>
        <$ButtonContainer>
          <Button buttonText={"ZAMKNIJ"} onClick={handleClose}></Button>
          <Button
            buttonText={"POBIERZ"}
            onClick={() => handleSubmit(name)}
          ></Button>
        </$ButtonContainer>
      </$Notification>
    </$Popup>
  );
};

export default Popup;
