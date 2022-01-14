import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useEffect, useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import SuccessPopup from 'src/components/utils/successPopup/SuccessPopup';

const LevelTwo = ({ title, setLevel }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    console.log(popupOpen);
  }, []);
  return (
    <$Level>
      <EditorConsole
        height='98%'
        level={'2'}
        width='95vw'
        language='markdown'
        setCompleted={setCompleted}
      />
      {completed ? (
        <SuccessPopup
          width='400px'
          height='200px'
          completed={() => {
            setLevel(3);
          }}
        ></SuccessPopup>
      ) : null}
      <Popup
        open={popupOpen}
        setOpen={setPopupOpen}
        width='300px'
        height='200px'
      >
        <div>Here is simple JSON file that you need to</div>
      </Popup>
    </$Level>
  );
};

export default LevelTwo;
