import { Props } from './types';
import './LevelOne.style.ts';
import EditorConsole from 'src/components/utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from 'src/components/utils/popup/Popup';
import { $LevelOne } from './LevelOne.style';

const LevelOne = ({ title }: Props) => {
  const [popupOpen, setPopupOpen] = useState(true);

  return (
    <$LevelOne>
      <EditorConsole
        height='100%'
        level={'1'}
        width='95vw'
        language='markdown'
      />

      <Popup
        open={popupOpen}
        setOpen={setPopupOpen}
        width='300px'
        height='200px'
      >
        <div>
          You haven't been working on that project for a long time. Now you want
          to change the readme.md file but you get a conflict! Fix that and push
          your version of the file. Good Luck!
        </div>
      </Popup>
    </$LevelOne>
  );
};

export default LevelOne;
