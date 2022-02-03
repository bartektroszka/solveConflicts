import { useEffect, useState } from 'react';
import { getcurrentLevel, getFolderTree, initLevel } from './api/rests';
import { $App } from './App.style';
import LevelFour from './components/levels/levelFour/LevelFour';
import LevelOne from './components/levels/levelOne/LevelOne';
import LevelThree from './components/levels/levelThree/levelThree';
import LevelTwo from './components/levels/levelTwo/LevelTwo';
import LevelBar from './components/utils/levelBar/LevelBar';
import Popup from './components/utils/popup/Popup';

function App() {
  const [currentLevel, setCurrentLevel] = useState(0);
  const [availableLevels, setAvailableLevels] = useState([1])
  const [reset, setReset] = useState(false);
  const [resetText, setResetText] = useState('Niestety musisz zresetować poziom');
  const resetFunc = (message:string) => {setReset(true); setResetText(message)}
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
        setAvailableLevels={(levels: number[]) => {
          setAvailableLevels(levels);
        }}
        reset={resetFunc}
      />
    ),
    2: (
      <LevelTwo
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
        setAvailableLevels={(levels: number[]) => {
          setAvailableLevels(levels);
        }}
        reset={resetFunc}

      />
    ),
    3: (
      <LevelThree
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
        setAvailableLevels={(levels: number[]) => {
          setAvailableLevels(levels);
        }}
        reset={resetFunc}
      />
    ),
    4: (
      <LevelFour
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
        setAvailableLevels={(levels: number[]) => {
          setAvailableLevels(levels);
        }}
        reset={resetFunc}
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
        {resetText}
      </Popup>
      <LevelBar 
        numberOfLevels={8} 
        currentLevel={currentLevel} 
        availableLevels={availableLevels}
        setLevel={(level: number) => {initLevel(`${level}`)
          .then((response) => {
            if(response.status === 200){
              setCurrentLevel(level); 
            }
      })}}></LevelBar>
    </$App>
  );
}

export default App;
