export interface Size {
  width: string;
  height: string;
}

export interface Props extends Size {
  numberOfLevels: number;
  currentLevel: number;
}
