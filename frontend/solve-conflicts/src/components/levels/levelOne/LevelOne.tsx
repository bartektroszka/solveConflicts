import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';

const LevelOne = ({ title, setLevel }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const [completed, setCompleted] = useState(false);
  console.log('kot');
  const handleExecutionResponse = (response: any) => {
    console.log(response);
    if (response.data.success === 'success') {
      setCompleted(true);
    }
    if (response.data.conflict) {
      setSecondPopupOpen(true);
    }
  };
  return (
    <$Level>
      <EditorConsole
        height='98%'
        level={'1'}
        width='95vw'
        executionResponseCallback={handleExecutionResponse}
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
          the przepis.txt file and merge branch
        </div>
      </Popup>
      <Popup
        open={secondPopupOpen}
        buttonText='CLOSE'
        afterClose={() => setSecondPopupOpen(false)}
        width='300px'
        height='200px'
      >
        <div>jasna dupa to conflict!</div>
      </Popup>
    </$Level>
  );
};

export default LevelOne;
