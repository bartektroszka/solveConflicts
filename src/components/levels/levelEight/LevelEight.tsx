import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import { initLevel } from 'src/api/rests';

const LevelEight= ({ setLevel, reset, setAvailableLevels }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const firedPopups = [1]
  const [completed, setCompleted] = useState(false);
  const handleExecutionResponse = (response: any) => {
    if (response.data.success) {
      setCompleted(true);
      if (response.data.reset) {
        reset(response.data.reset);
      }
    }
    if(response.data.stage == 2 && !firedPopups.includes(2)){
      setSecondPopupOpen(true)
      firedPopups.push(2)
    }
  };
  return (
    <$Level>
      <EditorConsole
        height='98%'
        level={'4'}
        width='100vw'
        executionResponseCallback={handleExecutionResponse}
      />

      <Popup
        open={completed}
        buttonText='NASTĘPNY POZIOM'
        afterClose={() => {
          initLevel('5').then((resp) => {
            setLevel(8);
          });
        }}
        width='300px'
        height='200px'
      >
        <img width='150px' height='150px' src='success.svg' alt='success'></img>
        Level Completed!
      </Popup>

      <Popup
        open={popupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setPopupOpen(false);
        }}
        width='500px'
        height='250px'
      >
        <div>
            Prowadzisz prace nad projektem programistycznym na gałęzi ‘master’.
            Na potrzeby naprawy kawałka kodu stworzyłeś gałąź bugFix i dokonałeś
            na niej kilku zmian. Twoim zadaniem jest dodanie tych zmian
            do głównego nurtu gałęzi. Możesz to zrobić za pomocą ‘merge’ lub ‘rebase’
        </div>
      </Popup>
      <Popup
        open={secondPopupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setSecondPopupOpen(false);
        }}
        width='500px'
        height='250px'
      >
        <div>
            A jednak powstał konflikt. Rozwiąż go i odbierz swój wymarzony dyplom ukończenia kursu!
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelEight;
