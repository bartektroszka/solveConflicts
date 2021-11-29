import axios, { AxiosPromise } from 'axios';
import { FolderTreeData } from 'src/components/utils/folderTree/types';

const url = 'http://127.0.0.1:5000';

const api = axios.create({
  baseURL: url,
});

export const execute = (cmd: string) => {
  return api.post('/execute', {
    command: cmd,
  });
};

export const getFolderTree = (): AxiosPromise => {
  return api.post('/get_tree', {
    nick: 'cisns',
  });
};

export const postFolderTree = (folderTree: FolderTreeData) => {
  return api.post('/save_tree', { tree: folderTree, nick: 'dupa' });
};
