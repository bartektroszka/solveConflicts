import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import { initLevel } from 'src/api/rests';

const LevelOne = ({ setLevel, reset }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const [thirdPopupOpen, setThirdPopupOpen] = useState(false);

  const [completed, setCompleted] = useState(false);
  const handleExecutionResponse = (response: any) => {
    if (response.data.success) {
      setCompleted(true);
    }
    if (response.data.conflict) {
      setThirdPopupOpen(true);
    }
    if (response.data.reset) {
      reset(response.data.reset);
    }
  };
  return (
    <$Level>
      <EditorConsole
        height='98%'
        level={'1'}
        width='100vw'
        executionResponseCallback={handleExecutionResponse}
      />
      <Popup
        open={completed}
        buttonText='NASTĘPNY POZIOM'
        afterClose={() => {
          initLevel('2').then((resp) => {
            setLevel(2);
          });
        }}
        width='400px'
        height='250px'
      >
        <img width='150px' height='150px' src='success.svg' alt='success'></img>
        Przeszedłeś Poziom!
      </Popup>
      <Popup
        open={popupOpen}
        buttonText='DALEJ'
        afterClose={() => {
          setPopupOpen(false);
          setSecondPopupOpen(true);
        }}
        width='600px'
        height='200px'
      >
        <div>
          Witaj w solveConflicts! Mamy nadzieję, że spólnie nauczymy się czegoś
          ciekawego o rozwiązywaniu konfliktów w systemie kontroli wersji GIT.
        </div>
      </Popup>
      <Popup
        open={secondPopupOpen}
        buttonText='ZAMKNIJ'
        afterClose={() => setSecondPopupOpen(false)}
        width='600px'
        height='300px'
      >
        <div>
          Razem ze swoim kolegą planujecie umieścić na swojej stronie
          internetowej przepis na naleśniki. W tym celu każdy z Was napisał
          własny przepis, ale teraz musisz zadecydować, który przepis jest
          lepszy i zostanie opublikowany. Po wpisaniu komendy: git branch
          zauważysz że znajdujesz się aktualnie na gałęzi ‘master’, gdzie jest
          plik z Twoją wersją przepisu. Twój kolega ma przepis na osobniej
          gałęzi (friend_branch). Spróbuj automatycznie połączyć te dwie gałęzie
          przy użyciu komendy: git merge friend_branch
        </div>
      </Popup>
      <Popup
        open={thirdPopupOpen}
        buttonText='ZAMKNIJ'
        afterClose={() => setThirdPopupOpen(false)}
        width='600px'
        height='270px'
      >
        <div>
          Niestety… zawartości plików są istotnie różne i GIT nie jest w stanie
          ich automatycznie połączyć. Zauważ, że zawartość pliku ‘przepis.txt’
          uległa zmianie. Znajdują się w nim teraz dwie wyraźnie oddzielone
          sekcje. Twoim zadaniem jest zmodyfikować ten plik wybierając jedną z
          dwóch wersji, po czym wykonanie komend: git add przepis.txt oraz git
          commit -m |wiadomość|
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelOne;
