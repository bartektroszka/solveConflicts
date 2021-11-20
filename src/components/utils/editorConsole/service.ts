import { execute } from 'src/api/rests';

export const sendCommand = (cmd: string) => {
  execute(cmd);
};
