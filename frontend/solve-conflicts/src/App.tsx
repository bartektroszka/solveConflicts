import { useEffect, useState } from "react";
import { getcurrentLevel, getFolderTree, initLevel } from "./api/rests";
import { $App } from "./App.style";
import { Level } from "./components/levels/Level";
import { levels } from "./components/levels/Levels";
import LevelBar from "./components/utils/levelBar/LevelBar";
import Popup from "./components/utils/popup/Popup";

function App() {
  const [currentLevel, setCurrentLevel] = useState<number>(1);
  const [completedLevels, setCompletedLevels] = useState([1]);
  const [reset, setReset] = useState(false);
  const [resetText, setResetText] = useState(
    "Niestety musisz zresetować poziom"
  );
  const resetFunc = (message: string) => {
    setReset(true);
    setResetText(message);
  };
  useEffect(() => {
    getcurrentLevel().then((response: any) => {
      setCurrentLevel(response.data.level);
    });
  }, []);
  return (
    <$App>
      <Level
        setLevel={(level: number) => setCurrentLevel(level)}
        levelNumber={currentLevel}
        popups={levels[currentLevel - 1]}
        setCompletedLevels={(levels: number[]) => setCompletedLevels(levels)}
        reset={resetFunc}
      ></Level>
      <Popup
        open={reset}
        buttonText="RESETUJ"
        afterClose={() => {
          setReset(false);
          window.location.reload();
        }}
        width="300px"
        height="200px"
      >
        {resetText}
      </Popup>
      <LevelBar
        numberOfLevels={8}
        currentLevel={currentLevel}
        completedLevels={completedLevels}
        setLevel={(level: number) => {
          initLevel(`${level}`).then((response) => {
            if (response.status === 200) {
              setCurrentLevel(level);
            }
          });
        }}
      ></LevelBar>
    </$App>
  );
}

export default App;
