import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import { initLevel } from 'src/api/rests';

const LevelThree = ({ setLevel, reset }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const [thirdPopupOpen, setThirdPopupOpen] = useState(false);
  const [completed, setCompleted] = useState(false);
  const handleExecutionResponse = (response: any) => {
    if (response.data.success) {
      setCompleted(true);
    }
    if (response.data.reset) {
      reset();
    }
    if (response.data.conflict) {
      setThirdPopupOpen(true);
    }
  };
  return (
    <$Level>
      <EditorConsole
        height='98%'
        level={'2'}
        width='100vw'
        executionResponseCallback={handleExecutionResponse}
      />

      <Popup
        open={completed}
        buttonText='NASTĘPNY POZIOM'
        afterClose={() => {
          initLevel('4').then((resp) => {
            setLevel(4);
          });
        }}
        width='300px'
        height='200px'
      >
        <img width='150px' height='150px' src='success.svg' alt='success'></img>
        Level completed!
      </Popup>

      <Popup
        open={popupOpen}
        buttonText='DALEJ'
        afterClose={() => {
          setPopupOpen(false);
          setSecondPopupOpen(true);
        }}
        width='500px'
        height='250px'
      >
        <div>
          Całkiem nieźle! Udało Ci się rozwiązać już dwa konflikty. Ale czy
          conflikt może wystąpić jedynie przy próbie wykonania ‘git merge’?
          Okazuje się, że konflikty mogą pojawiać się również przy innych
          komendach zmieniających strukturę repozytorium.
        </div>
      </Popup>
      <Popup
        open={secondPopupOpen}
        buttonText='ZAMKNIJ'
        afterClose={() => {
          setSecondPopupOpen(false);
        }}
        width='500px'
        height='300px'
      >
        <div>
          Jedną z nich jest git rebase. Pomoże nam ono uporządkować historię
          naszego repozytorium. Pracowałeś ostatnio nad dwiema gałęźni, gdzie
          jedna z nich wyliczała liczby Catalana, a na drugiej umieściłeś kod do
          wyliczania szeregu Taylora dla pewnych funkcji. Postanowiłeś, że
          możesz połączyć ten plik w jeden i sprawić żeby historia wyglądała
          tak, jakbyś nigdy nie rozdzielał pracy na dwoje, ale napotkałeś na
          pewien problem.
        </div>
      </Popup>
      <Popup
        open={thirdPopupOpen}
        buttonText='ZAMKNIJ'
        afterClose={() => {
          setThirdPopupOpen(false);
        }}
        width='500px'
        height='250px'
      >
        <div>
          Jedna z funkcji jest przyczyną problemu. Wybierz, z której
          implementacji wolałbyś korzystać i rozwiąż konflikt!
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelThree;
