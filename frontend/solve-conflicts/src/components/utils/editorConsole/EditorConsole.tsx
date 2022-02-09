import 'codemirror/lib/codemirror.css';
import 'codemirror/theme/material.css';
import 'codemirror/mode/xml/xml';
import 'codemirror/mode/javascript/javascript';
import 'codemirror/mode/python/python';
import { cpp } from '@codemirror/lang-cpp';
import 'codemirror/mode/markdown/markdown';
import { saveAs } from 'file-saver';
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
  $ButtonsContainer,
  $EmptyLine,
} from './EditorConsole.style';
import Terminal from 'terminal-in-react';
import FolderTree from '../folderTree/FolderTree';
import { Button } from '../button/Button';
import {
  execute,
  getFolderTree,
  postFolderTree,
  printDiploma,
} from 'src/api/rests';
import { useEffect, useState } from 'react';
import { Node } from '../folderTree/types';
import { GitTree } from 'src/components/utils/gitTree/GitTree';
import { GitCommit } from '../gitTree/types';
import { findNode } from './helpers';
import { IconButton } from '../iconButton/IconButton';
import DiplomaPopup from '../diplomaPopup/DiplomaPopup';

const EditorConsole = ({
  width,
  height,
  levelNumber,
  showTask,
  diplomaAvailable,
  executionResponseCallback,
}: Props) => {
  const [content, setContent] = useState('You can pass markdown code here');
  const [folderTree, setFolderTree] = useState<Node[]>([]);
  const [modified, setModified] = useState<boolean>(false);
  const [file, setFile] = useState<Node>({
    parentId: 0,
    id: 0,
    label: '',
    data: '',
  });
  const [gitTree, setGitTree] = useState<GitCommit[]>([]);
  const [gitTreeKey, setGitTreeKey] = useState<number>(0);
  const [buttonLoading, setButtonLoading] = useState<boolean>(false);
  const [diplomaPopupOpen, setDiplomaPopupOpen] = useState<boolean>(false);
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
  const saveFile = (name: string) => {
    setDiplomaPopupOpen(false);
    printDiploma(name).then((resp) => {
      let file = new File([resp.data], 'dyplom.html', {
        type: 'text/html;charset=utf-8',
      });
      saveAs(file, 'dyplom.html');
    });
  };
  const handleChange = (editor: () => void, data: string, value: string) => {
    setModified(true);
    setContent(value);
    setFile({ ...file, data: value });
    setFolderTree(editFolderTreeWithFile(folderTree, { ...file, data: value }));
  };
  const handleCommand = (cmd: any, print: any) => {
    execute(cmd.join(' ')).then((response) => {
      if (!gitTree.length) {
        setGitTree(response.data.git_tree);
        setGitTreeKey(Math.random());
      }
      const textResponse = response.data.stdout + response.data.stderr;
      executionResponseCallback(response);
      if (textResponse) print(textResponse);
      if (response.data.tree_change) {
        getFolderTree().then((response) => {
          setFolderTree(response.data.tree);
        });
      }
      if (response.data.git_change) {
        setGitTree(response.data.git_tree);
        setGitTreeKey(Math.random());
      }
    });
  };
  const handleSave = () => {
    setModified(false);
    setButtonLoading(true);
    postFolderTree(folderTree).then((response) => {
      setTimeout(function () {
        setButtonLoading(false);
      }, 500);
    });
  };

  const handleKeypress = (e: any) => {
    if (e.ctrlKey && e.keyCode === 83) {
      handleSave();
    }
  };

  useEffect(() => {
    let tempFile = findNode(file, folderTree);
    setFile(tempFile);
    setContent(tempFile.data ?? '');
  }, [folderTree]);

  useEffect(() => {
    getFolderTree().then((response) => {
      setFolderTree(response.data.tree);
      handleCommand(['git', 'status'], () => {});
    });
  }, [levelNumber]);

  return (
    <$AllContainer width={width} height={height} onKeyDown={handleKeypress}>
      <$ButtonsContainer>
        <IconButton
          icon='task'
          buttonText='polecenie'
          onClick={() => {
            showTask();
          }}
          width='8rem'
          height='2.2rem'
          active={true}
        />
        <IconButton
          icon='diploma'
          buttonText='dyplom'
          onClick={() => setDiplomaPopupOpen(true)}
          width='8rem'
          height='2.2rem'
          active={diplomaAvailable}
        />
      </$ButtonsContainer>
      <$EditorConsoleContainer>
        <$GitTreeContainer>
          <$EmptyLine></$EmptyLine>
          <GitTree key={gitTreeKey} commits={gitTree}></GitTree>
        </$GitTreeContainer>
        <$EditorContainer>
          <ControlledEditor
            onBeforeChange={handleChange}
            value={content}
            className='code-mirror-wrapper'
            options={{
              lineWrapping: true,
              lint: true,
              extensions: levelNumber === 4 ? [cpp()] : [],
              mode: {
                name:
                  file.label.split('.').pop() === 'txt' ||
                  file.label.split('.').pop() === 'lor'
                    ? 'markdown'
                    : 'python',
                json: true,
              },
              theme: 'material',
              lineNumbers: true,
            }}
          />
          <$BottomLine>
            <Button
              buttonText='zapisz'
              onClick={handleSave}
              loading={buttonLoading}
              buttonLoadingText='zapisywanie...'
              highlighted={modified}
            />
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
            commands={{
              help: (args: any, print: any, cmd: any) => {
                handleCommand(args, print);
              },
              show: (args: any, print: any, cmd: any) => {
                handleCommand(args, print);
              },
            }}
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
            if (node.label !== file.label) setModified(false);
            let copy = { ...node };
            setFile(copy);
            setContent(copy.data ?? '');
          }}
        ></FolderTree>
      </$EditorConsoleContainer>
      {diplomaPopupOpen ? (
        <DiplomaPopup
          handleClose={() => setDiplomaPopupOpen(false)}
          handleSubmit={(name) => {
            saveFile(name);
          }}
        ></DiplomaPopup>
      ) : null}
    </$AllContainer>
  );
};
export default EditorConsole;
