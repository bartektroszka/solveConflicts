import { Props } from './types';
import {
  $LevelBar,
  $CompletedLevel,
  $CurrentLevel,
  $FutureLevel,
  $AvailableLevel,
} from './LevelBar.style';

export const LevelBar = ({ numberOfLevels, currentLevel, setLevel, availableLevels }: Props) => {
  const returnLevel = (levelIndex: number) => {
    if(levelIndex + 1 === currentLevel){
      return (
        <$CurrentLevel width={'100%'} height={'42px'}>
          {levelIndex+1}
        </$CurrentLevel>)
    }
    else if(levelIndex + 1 === availableLevels.length){
      return (
        <$AvailableLevel width={'100%'} height={'42px'} key={levelIndex} onClick={(e) => setLevel(levelIndex+1)}>
          {levelIndex+1}
        </$AvailableLevel>)
    }
    else if(levelIndex + 1 < availableLevels.length){
      return (
        <$CompletedLevel width={'100%'} height={'42px'} key={levelIndex} onClick={(e) => setLevel(levelIndex+1)}>
          {levelIndex+1}
        </$CompletedLevel>)
    }
    else{
      return (
        <$FutureLevel width={'100%'} height={'42px'} key={levelIndex}>
          {levelIndex+1}
        </$FutureLevel>)
    }

  }
  return (
    <>
      <$LevelBar>
        {Array.from({ length: numberOfLevels}, (_, k) => (
          <>
            {returnLevel(k)}
          </>
        ))}
      </$LevelBar>
    </>
  );
};

export default LevelBar;
