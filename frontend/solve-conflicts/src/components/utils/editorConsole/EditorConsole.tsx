import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/material.css';
import 'codemirror/mode/xml/xml';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/python/python';
import 'codemirror/mode/markdown/markdown';

import 'codemirror/mode/xml/xml';
import 'codemirror/mode/css/css';
import { Controlled as ControlledEditor } from 'react-codemirror2';
import { Props } from './types';
import './EditorConsole.css';
import {
  $EditorConsoleContainer,
  $ConsoleContainer,
} from './EditorConsole.style';
import Terminal from 'terminal-in-react';
import { sendCommand } from './service';

const EditorConsole = ({ width, height, language, value, onChange }: Props) => {
  const handleChange = (editor: () => void, data: string, value: string) => {
    onChange(value);
  };
  const handleCommand = (cmd: string) => {
    sendCommand(cmd);
  };
  return (
    <$EditorConsoleContainer width={width} height={height}>
      <ControlledEditor
        onBeforeChange={handleChange}
        value={value}
        className='code-mirror-wrapper'
        options={{
          lineWrapping: true,
          lint: true,
          mode: language,
          theme: 'material',
          lineNumbers: true,
        }}
      />
      <$ConsoleContainer>
        <Terminal
          actionHandlers={{
            handleClose: (toggleClose) => {},
          }}
          startState='maximised'
          allowTabs={false}
          color='green'
          backgroundColor='black'
          barColor='black'
          style={{
            fontWeight: 'bold',
            fontSize: '1em',
            overflow: 'hidden !important',
          }}
          commandPassThrough={(cmd) => handleCommand(cmd)}
          msg='You can write only git commands.'
        />
      </$ConsoleContainer>
    </$EditorConsoleContainer>
  );
};
export default EditorConsole;
