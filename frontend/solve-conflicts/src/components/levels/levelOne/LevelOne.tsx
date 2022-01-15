import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';

const LevelOne = ({ title, setLevel }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [completed, setCompleted] = useState(false);

  return (
    <$Level>
      <EditorConsole
        height='98%'
        level={'1'}
        width='95vw'
        setCompleted={setCompleted}
      />
      {completed ? (
        <Popup
          open={popupOpen}
          buttonText='NEXT LEVEL'
          afterClose={() => setLevel(2)}
          width='300px'
          height='200px'
        >
          <img
            width='150px'
            height='150px'
            src='success.svg'
            alt='success'
          ></img>
          Level Completed!
        </Popup>
      ) : null}
      <Popup
        open={popupOpen}
        buttonText='CLOSE'
        afterClose={() => setPopupOpen(false)}
        width='300px'
        height='200px'
      >
        <div>
          You have come up with a great pancake recipe. Now you want to change
          the readme.md file but you get a conflict! Someone thinks that there
          are better pancakes than yours! Fix that and merge. Good Luck!
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelOne;
