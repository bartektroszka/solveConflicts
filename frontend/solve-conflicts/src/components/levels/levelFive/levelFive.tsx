import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import { initLevel } from 'src/api/rests';

const LevelFive = ({ setLevel, reset, setAvailableLevels }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const [thirdPopupOpen, setThirdPopupOpen] = useState(false);
  const [completed, setCompleted] = useState(false);
  const handleExecutionResponse = (response: any) => {
    if (response.data.success) {
      setCompleted(true);
      if (response.data.reset) {
        reset(response.data.reset);
      }
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
          initLevel('6').then((resp) => {
            setLevel(6);
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
          setSecondPopupOpen(true);
        }}
        width='500px'
        height='250px'
      >
        <div>
            Ten poziom, będzie krótką odskocznią od rozwiązywania konfliktów, ale
            też niesie w sobie nieco przydatnej wiedzy. Wyboraź sobie sytuację, gdzie
            w pracy dostałeś zlecenie na wykonanie połączenie dwóch (lub więcej)
            bardzo rozbudowanych gałęzi. Rozwiązałeś już część konfliktów, ale
            w trakcie pracy, Twój szef powiedział, żeby się jednak wstrzymać
            z mergowaniem, bo nie jest jeszcze do końca pewien, które wersje plików
            chciałby zostawić.
        </div>
      </Popup>

      <Popup
        open={secondPopupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setSecondPopupOpen(false);
          setThirdPopupOpen(true);
        }}
        width='500px'
        height='250px'
      >
        <div>
            Jedzie na urlop i wróci dopiero za tydzień, więc nie ma co
            bezczynnie czekać. W tej sytuacji należy zrezygnować z aktualnego stanu
            i próbować wrócić do prac na jednej z gałęzi. Jak to zrobić? Okazuje się,
            że sprawa jest bardzo prosta. Wystarczy wykonać komendę “git merge --abort”,
            aby repozytorium powróciło do stanu sprzed wywołania komendy merge.
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
            Okazuje się, że flaga --abort działa
            w bardzo podobny sposób, jeżeli chcielibyśmy cofnąć zmiany w trakcie
            ‘git rebase’ albo ‘git cherry-pick’
            [notka o tym, że --abort działa też dla rebase i cherry-pick???]
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelFive;
