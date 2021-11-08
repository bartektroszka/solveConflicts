import axios from 'axios';

const url = '127.0.0.1:5000';

export const execute = (cmd: string) =>
  axios({
    method: 'post',
    url: `${url}/execute`,
    data: cmd,
  });
