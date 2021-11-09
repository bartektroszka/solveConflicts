import { Props } from './types';
import './LevelOne.style.ts';
import EditorConsole from './../../utils/editorConsole/EditorConsole';
import { useState } from 'react';
import Popup from '../../utils/popup/Popup';

const LevelOne = ({ title }: Props) => {
  const [content, setContent] = useState('You can pass markdown code here');
  const [popupOpen, setPopupOpen] = useState(true);
  return (
    <div className='header'>
      <EditorConsole
        height='85vh'
        width='80vw'
        value={content}
        onChange={setContent}
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
    </div>
  );
};

export default LevelOne;
