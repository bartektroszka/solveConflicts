import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import { initLevel } from 'src/api/rests';

const LevelFour = ({ setLevel, reset, setAvailableLevels }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const [thirdPopupOpen, setThirdPopupOpen] = useState(false);
  const [fourthPopupOpen, setFourthPopupOpen] = useState(false);
  const [fifthPopupOpen, setFifthPopupOpen] = useState(false);
  const firedPopups = [1,2,3]
  const [completed, setCompleted] = useState(false);
  const handleExecutionResponse = (response: any) => {
    if (response.data.success) {
      setCompleted(true);
      if (response.data.reset) {
        reset(response.data.reset);
      }
    }
    if(response.data.stage == 2 && !firedPopups.includes(4)){
      setFourthPopupOpen(true)
      firedPopups.push(4)
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
            setLevel(5);
          });
        }}
        width='300px'
        height='200px'
      >
        <img width='150px' height='150px' src='success.svg' alt='success'></img>
        Przeszedłeś Poziom!
      </Popup>

      <Popup
        open={popupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setPopupOpen(false);
          setSecondPopupOpen(true);
          firedPopups.push(2)
        }}
        width='500px'
        height='250px'
      >
        <div>
          Razem z kilkoma znajomymi postanowiliście wystąpić w drużynowym konkursie
          programistycznym. Polega on na tym, że każdy próbuje wymyślić swoją
          strategię na rozwiązanie problemu optymalizacyjnego, a po jakimś czasie
          i naradach drużyna przechodzi w tryb implementacji kodu.
        </div>
      </Popup>
      <Popup
        open={secondPopupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setSecondPopupOpen(false);
          setThirdPopupOpen(true);
          firedPopups.push(3)
        }}
        width='500px'
        height='250px'
      >
        <div>
          Wpadłeś na bardzo skomplikowany, ale obiecujący pomysł. Niestety
          wymyślenie go zabrało Ci trochę czasu. Chcesz go nadrobić. Pomyślałeś
          więc, że skorzystasz z szablonu kodu, który w międzyczasie zdąrzył już
          napisać jeden z Twoich kolegów. Wykonał on już kilka commitów na gałęzi
          swojego kodu, ale dla Ciebie
          istotny jest tylko jeden z nich o nazwie “defines”. W tym commicie jest
          kilka przydatnych linii kodu, których nie ma sensu przepisywać
          automatycznie.
        </div>
      </Popup>
      <Popup
        open={thirdPopupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setThirdPopupOpen(false);
        }}
        width='500px'
        height='250px'
      >
        <div>
          Za pomocą “git cherry-pick COMMIT” wyłuskaj commit, którego
          potrzebujesz i dołącz go do swojej gałęzi, a jeżeli w międzyczasie pojawi
          się również jakiś konflikt, to go rozwiąż!
        </div>
      </Popup>
      <Popup
        open={fourthPopupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setFourthPopupOpen(false);
          setFifthPopupOpen(true)
          firedPopups.push(5)
        }}
        width='500px'
        height='250px'
      >
        <div>
        A niech to! Znowu jeden z tych przeklętych konfliktów! Na pewno dasz sobie z nim radę
        </div>
      </Popup>
      <Popup
        open={fifthPopupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setFifthPopupOpen(false);
        }}
        width='500px'
        height='250px'
      >
        <div>
          Może wydawać się to dziwne, ale jedna z sekcji powstałych w pliku
          konfliktowym jest pusta, ale oznacza, że git oznacza brak zmian, jako zmianę.
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelFour;
