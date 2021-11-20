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
  $AllContainer,
  $BottomLine,
} from './EditorConsole.style';
import Terminal from 'terminal-in-react';
import FolderTree from '../folderTree/FolderTree';
import { Button } from '../button/Button';
import { execute, getFolderTree, postFolderTree } from 'src/api/rests';
import { useEffect, useState } from 'react';
import { FolderTreeData } from '../folderTree/types';

const EditorConsole = ({ width, height, language, level }: Props) => {
  const handleChange = (editor: () => void, data: string, value: string) => {
    setContent(data);
  };
  const handleCommand = (cmd: string) => {
    execute(cmd);
  };

  const [content, setContent] = useState('You can pass markdown code here');
  const [folderTree, setFolderTree] = useState<FolderTreeData>([
    {
      id: 12345678,
      parentId: null,
      label: 'My parent node',
      items: [
        {
          id: 87654321,
          label: 'My file',
          parentId: 12345678,
          data: 'siema eniu',
        },
      ],
    },
    {
      id: 56789012,
      parentId: 12345678,
      label: 'My child node',
      items: [
        {
          id: 876543,
          label: 'My file2',
          parentId: 56789012,
          data: 'bam barararara',
        },
      ],
    },
  ]);

  useEffect(() => {
    getFolderTree(level).then((response) => {
      setFolderTree(response.data);
    });
  }, [level]);

  useEffect(() => {
    console.log(folderTree);
    postFolderTree(level, folderTree);
  }, [folderTree, level]);

  return (
    <$AllContainer width={width} height={height}>
      <$EditorConsoleContainer>
        <ControlledEditor
          onBeforeChange={handleChange}
          value={content}
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
        <FolderTree
          data={folderTree}
          setContent={(val) => setContent(val)}
        ></FolderTree>
      </$EditorConsoleContainer>
      <$BottomLine>
        <Button buttonText='save' onClick={() => {}} />
      </$BottomLine>
    </$AllContainer>
  );
};
export default EditorConsole;
