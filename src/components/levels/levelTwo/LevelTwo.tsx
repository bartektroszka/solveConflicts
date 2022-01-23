import { Props } from '../types';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $Level } from '../Levels.style';
import { initLevel } from 'src/api/rests';

const LevelTwo = ({ setLevel, reset }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);
  const [secondPopupOpen, setSecondPopupOpen] = useState(false);
  const [completed, setCompleted] = useState(false);
  const handleExecutionResponse = (response: any) => {
    if (response.data.success) {
      setCompleted(true);
    }
    if (response.data.reset) {
      reset();
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
          initLevel('3').then((resp) => {
            setLevel(3);
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
        buttonText='DALEJ'
        afterClose={() => {
          setPopupOpen(false);
          setSecondPopupOpen(true);
        }}
        width='500px'
        height='250px'
      >
        <div>
          Pierwszy poziom był dość prosty. Teraz będzie nieco trudniej. Masz za
          zadanie połączyć dwie wersje pliku ‘style.json’ z konfguracą
          stylowania Waszej strony internetowej. W tym pliku są trzy sekcje
          (“header”, “main-table” oraz “footer”).
        </div>
      </Popup>
      <Popup
        open={secondPopupOpen}
        buttonText='ZAMKNIJ'
        afterClose={() => {
          setSecondPopupOpen(false);
        }}
        width='500px'
        height='250px'
      >
        <div>
          O ile obie wersje pliku mają taką samą wersję sekcji “main-table”, to
          pozostałe sekcje się od siebie różnią. Wspólnie z kolegą ustaliliście,
          aby zachować Twoją wersję kawałka odpowiadającego za sekcję “footer”,
          ale wersję Twojego kolegi jeżeli chodzi o “header”. Do dzieła!
          Polecamy rozpocząć od komend: git branch oraz git merge
        </div>
      </Popup>
    </$Level>
  );
};

export default LevelTwo;
