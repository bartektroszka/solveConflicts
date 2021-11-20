import axios, { AxiosPromise } from 'axios';
import { FolderTreeData } from 'src/components/utils/folderTree/types';

const url = 'http://127.0.0.1:5000';

const api = axios.create({
  baseURL: url,
});

export const execute = (cmd: string) => {
  api.post('/execute', {
    command: cmd,
  });
};

export const getFolderTree = (level: string): AxiosPromise => {
  return api.get('/foldertree', { data: { level } });
};

export const postFolderTree = (level: string, folderTree: FolderTreeData) => {
  return api.post('/foldertree', { data: { level, folderTree } });
};
