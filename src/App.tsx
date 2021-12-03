import { $App } from './App.style';
import LevelOne from './components/levels/levelOne/LevelOne';
import LevelBar from './components/utils/levelBar/LevelBar';

function App() {
  return (
    <$App>
      <LevelOne title='Level 1' />
      <LevelBar numberOfLevels={8} currentLevel={2}></LevelBar>
    </$App>
  );
}

export default App;
