import { $App } from './App.style';
import LevelOne from './components/levels/levelOne/LevelOne';
import LevelBar from './components/utils/levelBar/LevelBar';

function App() {
  return (
    <$App>
      <LevelOne title='Level 1' />
      <LevelBar
        numberOfLevels={8}
        currentLevel={1}
        width='100%'
        height='3rem'
      ></LevelBar>
    </$App>
  );
}

export default App;
