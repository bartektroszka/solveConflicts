import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import SuccessPopup from 'src/components/utils/successPopup/SuccessPopup';

const LevelOne = ({ title, setLevel }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [completed, setCompleted] = useState(false);

  return (
    <$Level>
      <EditorConsole
        height='98%'
        level={'1'}
        width='95vw'
        language='markdown'
        setCompleted={setCompleted}
      />
      {completed ? (
        <SuccessPopup
          width='400px'
          height='200px'
          completed={() => {
            setLevel(2);
          }}
        ></SuccessPopup>
      ) : null}
      <Popup
        open={popupOpen}
        setOpen={setPopupOpen}
        width='300px'
        height='200px'
      >
        <div>
          You haven't been working on that project for a long time. Now you want
          to change the readme.md file but you get a conflict! Fix that and push
          your version of the file. Good Luck!
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelOne;
