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
  $EditorContainer,
  $GitTreeContainer,
} from './EditorConsole.style';
import Terminal from 'terminal-in-react';
import FolderTree from '../folderTree/FolderTree';
import { Button } from '../button/Button';
import { execute, getFolderTree, postFolderTree } from 'src/api/rests';
import { useEffect, useState } from 'react';
import { Node } from '../folderTree/types';
import { GitTree } from 'src/components/utils/gitTree/GitTree';
import { GitCommit } from '../gitTree/types';
import { findNode } from './helpers';

const EditorConsole = ({
  width,
  height,
  language,
  level,
  setCompleted,
}: Props) => {
  const [content, setContent] = useState('You can pass markdown code here');
  const [folderTree, setFolderTree] = useState<Node[]>([]);
  const [file, setFile] = useState<Node>({
    parentId: 0,
    id: 0,
    label: '',
    data: '',
  });
  const [gitTree, setGitTree] = useState<GitCommit[]>([]);

  const editFolderTreeWithFile = (treeData: Node[], file: Node) => {
    let copy: Node[] = [];
    treeData.forEach((element) => {
      if (element.id === file.id) {
        copy.push(file);
      } else if (element.items) {
        let items_array: Node[] = [];
        element.items.forEach((el) => {
          if (el.id === file.id) {
            items_array.push(file);
          } else {
            items_array.push(el);
          }
        });
        copy.push({ ...element, items: items_array });
      } else {
        copy.push(element);
      }
    });
    return copy;
  };
  const handleChange = (editor: () => void, data: string, value: string) => {
    setContent(value);
    setFile({ ...file, data: value });
    setFolderTree(editFolderTreeWithFile(folderTree, { ...file, data: value }));
  };
  const handleCommand = (cmd: any, print: any) => {
    execute(cmd.join(' ')).then((response) => {
      const textResponse = response.data.stdout + response.data.stderr;
      const tree = response.data.git_tree;
      setGitTree(tree);
      if (textResponse) print(textResponse);
      if (response.data.success) {
        setCompleted(true);
      } else if (response.data.tree_change) {
        getFolderTree().then((response) => {
          setFolderTree(response.data);
        });
      }
    });
  };
  const handleSave = () => {
    postFolderTree(folderTree);
  };

  useEffect(() => {
    console.log('pieson');
    let temp_file = findNode(file, folderTree);
    console.log(temp_file, folderTree);
    setFile(temp_file);
    setContent(temp_file.data ?? '');
  }, [folderTree]);

  useEffect(() => {
    getFolderTree().then((response) => {
      setFolderTree(response.data);
    });
    handleCommand(['git', 'status'], () => {});
  }, []);

  return (
    <$AllContainer width={width} height={height}>
      <$EditorConsoleContainer>
        <$GitTreeContainer>
          <GitTree key={gitTree.length} commits={gitTree}></GitTree>
        </$GitTreeContainer>
        <$EditorContainer>
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
          <$BottomLine>
            <Button buttonText='save' onClick={handleSave} />
          </$BottomLine>
        </$EditorContainer>
        <$ConsoleContainer>
          <Terminal
            actionHandlers={{
              handleClose: (toggleClose) => {},
              handleMaximise: (toggleClose) => {},
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
              maxHeight: '100%',
            }}
            commandPassThrough={(cmd, print) => handleCommand(cmd, print)}
            msg='You can write only git commands.'
          />
        </$ConsoleContainer>
        <FolderTree
          data={folderTree}
          setFile={(node: Node) => {
            setFile(node);
            setContent(node.data ?? '');
          }}
        ></FolderTree>
      </$EditorConsoleContainer>
    </$AllContainer>
  );
};
export default EditorConsole;
