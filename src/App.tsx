import { useEffect, useState } from 'react';
import { getcurrentLevel, getFolderTree } from './api/rests';
import { $App } from './App.style';
import LevelFour from './components/levels/levelFour/LevelFour';
import LevelOne from './components/levels/levelOne/LevelOne';
import LevelThree from './components/levels/levelThree/levelThree';
import LevelTwo from './components/levels/levelTwo/LevelTwo';
import LevelBar from './components/utils/levelBar/LevelBar';
import Popup from './components/utils/popup/Popup';

function App() {
  const [currentLevel, setCurrentLevel] = useState(0);
  const [reset, setReset] = useState(false);
  useEffect(() => {
    getcurrentLevel().then((response: any) => {
      setCurrentLevel(response.data.level);
    });
  }, []);
  const levels: { [key: number]: React.ReactNode } = {
    1: (
      <LevelOne
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
        reset={() => setReset(true)}
      />
    ),
    2: (
      <LevelTwo
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
        reset={() => setReset(true)}
      />
    ),
    3: (
      <LevelThree
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
        reset={() => setReset(true)}
      />
    ),
    4: (
      <LevelFour
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
        reset={() => setReset(true)}
      />
    ),
  };
  return (
    <$App>
      {levels[currentLevel]}
      <Popup
        open={reset}
        buttonText='RESETUJ'
        afterClose={() => {
          setReset(false);
          window.location.reload();
        }}
        width='300px'
        height='200px'
      >
        Niestety, nabałaganiłeś i musisz zresetować poziom.
      </Popup>
      <LevelBar numberOfLevels={8} currentLevel={currentLevel}></LevelBar>
    </$App>
  );
}

export default App;
