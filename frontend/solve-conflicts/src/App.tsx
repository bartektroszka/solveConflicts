import { useEffect, useState } from 'react';
import { getcurrentLevel, getFolderTree } from './api/rests';
import { $App } from './App.style';
import LevelOne from './components/levels/levelOne/LevelOne';
import LevelTwo from './components/levels/levelTwo/LevelTwo';
import LevelBar from './components/utils/levelBar/LevelBar';

function App() {
  const [currentLevel, setCurrentLevel] = useState(1);
  useEffect(() => {
    getcurrentLevel().then((response: any) => {
      setCurrentLevel(response.data.level);
    });
  }, []);
  const levels: { [key: number]: React.ReactNode } = {
    1: (
      <LevelOne
        title='level 1'
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
      />
    ),
    2: (
      <LevelTwo
        title='level 2'
        setLevel={(levelNumber: number) => {
          setCurrentLevel(levelNumber);
        }}
      />
    ),
    3: null,
  };
  return (
    <$App>
      {levels[currentLevel]}
      <LevelBar numberOfLevels={8} currentLevel={currentLevel}></LevelBar>
    </$App>
  );
}

export default App;
