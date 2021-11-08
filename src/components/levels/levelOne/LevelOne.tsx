import { Props } from "./types";
import "./LevelOne.style.ts";
import EditorConsole from "./../../utils/editorConsole/EditorConsole";
import { useState } from "react";
import Popup from "../../utils/popup/Popup";

const LevelOne = ({ title }: Props) => {
  const [content, setContent] = useState("You can pass javascript code here");
  const [popupOpen, setPopupOpen] = useState(true)
  return (
    <div className="header">
      <EditorConsole
        height="85vh"
        width="80vw"
        value={content}
        onChange={setContent}
        language="javascript"
      />
      <Popup open={popupOpen} setOpen={setPopupOpen} width="300px" height="200px">
        <div>dupa</div>
      </Popup>
    </div>
  );
};

export default LevelOne;
