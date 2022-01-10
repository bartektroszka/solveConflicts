import { useState } from 'react';
import { $App } from './App.style';
import LevelOne from './components/levels/levelOne/LevelOne';
import LevelBar from './components/utils/levelBar/LevelBar';

function App() {
  const [currentLevel, setCurrentLevel] = useState(1);
  const levels: { [key: number]: React.ReactNode } = {
    1: (
      <LevelOne
        title='level 1'
        goNextLevel={() => {
          setCurrentLevel(1);
        }}
      />
    ),
  };
  return (
    <$App>
      {levels[currentLevel]}
      <LevelBar numberOfLevels={8} currentLevel={currentLevel}></LevelBar>
    </$App>
  );
}

export default App;
