import { Props } from './types';
import {
  $LevelBar,
  $CompletedLevel,
  $CurrentLevel,
  $FutureLevel,
} from './LevelBar.style';

export const LevelBar = ({ numberOfLevels, currentLevel }: Props) => {
  const numberOfCompletedLevels = currentLevel - 1;
  const numberOfFutureLevels = numberOfLevels - currentLevel;
  return (
    <>
      <$LevelBar>
        {Array.from({ length: numberOfCompletedLevels }, (_, k) => (
          <>
            <$CompletedLevel width={'100%'} height={'42px'} key={k}>
              {k + 1}
            </$CompletedLevel>
          </>
        ))}
        <$CurrentLevel width={'100%'} height={'42px'}>
          {currentLevel}
        </$CurrentLevel>
        {Array.from({ length: numberOfFutureLevels }, (_, k) => (
          <$FutureLevel width={'100%'} height={'42px'} key={k}>
            {currentLevel + k + 1}
          </$FutureLevel>
        ))}
      </$LevelBar>
    </>
  );
};

export default LevelBar;
