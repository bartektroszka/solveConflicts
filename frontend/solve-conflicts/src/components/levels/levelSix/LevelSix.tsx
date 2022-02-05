import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import { initLevel } from 'src/api/rests';

const LevelSix= ({ setLevel, reset, setAvailableLevels }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const [thirdPopupOpen, setThirdPopupOpen] = useState(false);
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
          initLevel('7').then((resp) => {
            setLevel(7);
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
        }}
        width='500px'
        height='250px'
      >
        <div>
            Razem z bratem planujecie wyjechać latem w góry pozdobywać Tatrzańskie
            szczyty. W tym celu postanowiliście zrobić kalendarz wypraw na szlaki.
            Każdy z Was podał jakieś propozycje tras, i teraz pora na połączenie
            pomysłów. Użyj komendy git merge!
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
            Niestety okazuje się, że merge się nawet nie rozpoczął… bo z pliku
            ‘wyjazd.txt’ znalazła się jakaś przypadkowa zmiana od ostatniego commita.
            W takiej sytuacji najlepiej byłoby pozbyć się tych niepotrzebnych zmian
            i wrócić do sytuacji bezpośrednio po zrobieniu ostatniego commita. Na
            szczęście Git daje nam taką możliwość! Z pomocą przychodzi komenda git restore.
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
            Użyj tej komendy by, przywrócić prawidłowy stan dla pliku wyjazd.txt,
            a następnie połącza gałęzie ‘pat’ i ‘mat’ (jeżeli zajdzie konflikt, to
            zadbaj o jego rozwiazanie)
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelSix;
