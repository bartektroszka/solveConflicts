import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import { initLevel } from 'src/api/rests';

const LevelSeven = ({ setLevel, reset, setAvailableLevels }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const [thirdPopupOpen, setThirdPopupOpen] = useState(false);
  const [fourthPopupOpen, setFourthPopupOpen] = useState(false);
  const [fifthPopupOpen, setFifthPopupOpen] = useState(false);
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
          initLevel('8').then((resp) => {
            setLevel(8);
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
        }}
        width='500px'
        height='250px'
      >
        <div>
            Postanowiłeś zrobić swoim rodzicom prezent! Na ich trzydziestą rocznicę
            ślubu chcesz zrobić im remont mieszkania. Nic prostszego… Już nawet
            przygotowałeś arkusz, w którym wpisałeś co chcesz im wyremontować.
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
            Jak to jednak w życiu bywa… rodzice po tym jak usłyszeli, że chcesz
            zrobić im prezent, postanowili wprowadzić pewne poprawki do arkusza…
            Stworzyli nawet nową gałąć w systemie GIT by tam notować swoje zmiany
        </div>
      </Popup>

      <Popup
        open={thirdPopupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setThirdPopupOpen(false)
          setFourthPopupOpen(true);
        }}
        width='500px'
        height='250px'
      >
        <div>
            Poprosili Cię o uwględnienie tych zmian… Sytuacja jest opłakana, ilość
            poprawek, które wprowadzili rodzice jest zatrważająca. Trudno Ci będzie w
            takiej sytuacji odmówić. Nie wiemy jak uratować Twój portfel, ale możemy
            pokazać Ci metodę na zaoszczędzenie czasu.
        </div>
      </Popup>
      <Popup
        open={fourthPopupOpen}
        buttonText='CLOSE'
        afterClose={() => {
          setFourthPopupOpen(false);
          setFifthPopupOpen(true);
        }}
        width='500px'
        height='250px'
      >
        <div>
            Dla komendy merge można podać flagę ‘-X’, która pozwala na określenie
            strategii przy merdżowaniu. i tak gdy podamy ‘-X ours’ to wszystkie
            konflikty będą rozstrzygane na korzyść HEAD, a dla ‘-X theirs’ na korzyść drugiej gałęzi.
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
            W tym poziomie, możesz albo spróbować wykonać wszystkie zmiany ręcznie
            (zawsze zostawiając wersje z gałęzi rodziców), albo po prostu skorzystać z flagi -X
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelSeven;
