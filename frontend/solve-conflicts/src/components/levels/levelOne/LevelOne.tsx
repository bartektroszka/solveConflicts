import { Props } from "./types";
import "./LevelOne.style.ts";
import EditorConsole from "./../../utils/editorConsole/EditorConsole";
import { useState } from "react";

const LevelOne = ({ title }: Props) => {
  const [content, setContent] = useState("You can pass javascript code here");
  return (
    <div className="header">
      <EditorConsole
        height="85vh"
        width="80vw"
        value={content}
        onChange={setContent}
        language="javascript"
      />
    </div>
  );
};

export default LevelOne;
