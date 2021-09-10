import { Props } from "./types";
import {
  $LevelBar,
  $CompletedLevel,
  $CurrentLevel,
  $FutureLevel,
} from "./LevelBar.style";

export const LevelBar = ({
  numberOfLevels,
  currentLevel,
  width,
  height,
}: Props) => {
  const numberOfCompletedLevels = currentLevel - 1;
  const numberOfFutureLevels = numberOfLevels - currentLevel;
  return (
    <$LevelBar width={width} height={height}>
      {Array.from({ length: numberOfCompletedLevels }, (_, k) => (
        <$CompletedLevel width={width} height={height} key={k}>
          {k + 1}
        </$CompletedLevel>
      ))}
      <$CurrentLevel width={width} height={height}>
        {currentLevel}
      </$CurrentLevel>
      {Array.from({ length: numberOfFutureLevels }, (_, k) => (
        <$FutureLevel width={width} height={height} key={k}>
          {currentLevel + k + 1}
        </$FutureLevel>
      ))}
    </$LevelBar>
  );
};

export default LevelBar;
