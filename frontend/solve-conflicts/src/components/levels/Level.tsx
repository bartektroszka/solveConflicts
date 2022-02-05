import { useEffect, useState } from "react";
import { initLevel } from "src/api/rests";
import EditorConsole from "../utils/editorConsole/EditorConsole";
import Popup from "../utils/popup/Popup";
import { $Level } from "./Levels.style";
import { Props } from "./types";

export const Level = ({
  popups,
  levelNumber,
  setLevel,
  setCompletedLevels,
  reset,
}: Props) => {
  const [currentPopup, setCurrentPopup] = useState<number>(0);
  const [stage, setStage] = useState<number>(1);
  const [completed, setCompleted] = useState<boolean>(false);
  const handleExecutionResponse = (response: any) => {
    setLevel(response.data.level);
    if (response.data.success) {
      setCompleted(true);
    }
    if (response.data.reset) {
      reset(response.data.reset);
    }
    if (response.data.completed) {
      setCompletedLevels(response.data.completed);
    }

    setStage(response.data.stage);
  };
  return (
    <$Level>
      <EditorConsole
        height="98%"
        width="100vw"
        levelNumber={levelNumber}
        executionResponseCallback={handleExecutionResponse}
        key={levelNumber}
      />
      {popups[currentPopup]?.stage === stage ? (
        <Popup
          open={stage === popups[currentPopup].stage}
          buttonText={"DALEJ"}
          afterClose={() => {
            setCurrentPopup(currentPopup + 1);
          }}
          width={popups[currentPopup].width}
          height={popups[currentPopup].height}
        >
          {popups[currentPopup].message}
        </Popup>
      ) : null}
      {
        <Popup
          open={completed}
          buttonText={"NASTĘPNY POZIOM"}
          afterClose={() => {
            initLevel(`${levelNumber + 1}`).then((resp) => {
              setLevel(levelNumber + 1);
              setCompleted(false);
            });
          }}
          width={"600px"}
          height={"300px"}
        >
          <img
            width="150px"
            height="150px"
            src="success.svg"
            alt="success"
          ></img>
          Udało Ci się rozwiązać zadanie!
        </Popup>
      }
    </$Level>
  );
};
