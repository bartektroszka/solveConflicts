import axios from "axios";

const url = "";

export const sendCommand = (cmd: string) => {
  axios.post(url, cmd);
};
