import axios from 'axios';

const url = 'http://127.0.0.1:5000';
const api = axios.create({
  baseURL: url,
});
export const execute = (cmd: string) =>
  api.post('/execute', {
    command: cmd,
  });
