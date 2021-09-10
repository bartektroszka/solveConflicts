import React from "react";
import { $App } from "./App.style";
import LevelOne from "./components/levels/levelOne/LevelOne";
import LevelBar from "./components/utils/levelBar/LevelBar";

function App() {
  return (
    <$App>
      <LevelOne title="Level 1" />
      <LevelBar
        numberOfLevels={12}
        currentLevel={4}
        width="100%"
        height="100px"
      ></LevelBar>
    </$App>
  );
}

export default App;
