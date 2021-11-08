import { execute } from 'api/rests';

export const sendCommand = (cmd: string) => {
  execute(cmd);
};
