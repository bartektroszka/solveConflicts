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
import { FolderTreeData, Node } from '../folderTree/types';
import { SnippetFolderSharp } from '@mui/icons-material';

const EditorConsole = ({ width, height, language, level }: Props) => {
  const [content, setContent] = useState('You can pass markdown code here');
  const [folderTree, setFolderTree] = useState<FolderTreeData>([]);
  const [file, setFile] = useState<Node>({
    parentId: 0,
    id: 0,
    label: '',
    data: '',
  });

  const handleChange = (editor: () => void, data: string, value: string) => {
    setContent(value);
    setFile({ ...file, data: value });
  };
  const handleCommand = (cmd: any) => {
    execute(cmd.join(' '));
  };
  const handleSave = () => {
    postFolderTree(folderTree);
  };

  useEffect(() => {
    getFolderTree().then((response) => {
      setFolderTree([response.data]);
    });
  }, [level]);

  useEffect(() => {
    const editFolderTreeWithFile = (treeData: FolderTreeData, file: Node) => {
      for (let i = 0; i < treeData.length; i++) {
        const node = treeData[i];
        if (node.id === file.id) treeData[i] = file;
        else if (node.items !== undefined) {
          editFolderTreeWithFile(node.items, file);
        }
      }
      return treeData;
    };

    setContent(file.data ?? '');
    setFolderTree(editFolderTreeWithFile(folderTree, file));
  }, [file, folderTree]);

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
          setFile={(node: Node) => {
            setFile(node);
          }}
        ></FolderTree>
      </$EditorConsoleContainer>

      <$BottomLine>
        <Button buttonText='save' onClick={handleSave} />
      </$BottomLine>
    </$AllContainer>
  );
};
export default EditorConsole;
