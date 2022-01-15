import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';

const LevelTwo = ({ title, setLevel }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [completed, setCompleted] = useState(false);

  return (
    <$Level>
      <EditorConsole
        height='98%'
        level={'2'}
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
          Here is simple JSON file that you edit to adjust appearance of your
          site. Merge It.
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelTwo;
