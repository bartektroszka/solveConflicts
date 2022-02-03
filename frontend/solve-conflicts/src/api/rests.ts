import axios, { AxiosPromise } from 'axios';
import { Node } from 'src/components/utils/folderTree/types';

const url = 'http://127.0.0.1:5000';

const api = axios.create({
  baseURL: url,
  withCredentials: true,
});

export const execute = (cmd: string) => {
  return api.post('/execute', {
    command: cmd,
  });
};

export const getFolderTree = (): AxiosPromise => {
  return api.get('/get_tree');
};

export const getcurrentLevel = (): AxiosPromise => {
  return api.get('/get_current_level');
};

export const initLevel = (levelNumber: string): AxiosPromise => {
  return api.post('/init_level', { level: levelNumber });
};

export const register = (): AxiosPromise => {
  return api.get('/register');
};

export const postFolderTree = (folderTree: Node[]) => {
  return api.post('/save_tree', { tree: folderTree[0] });
};
