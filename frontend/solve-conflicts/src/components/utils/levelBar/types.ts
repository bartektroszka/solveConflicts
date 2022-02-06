import { Size } from '../../../types';

export interface Props {
  numberOfLevels: number;
  currentLevel: number;
  completedLevels: number[];
  setLevel: (level:number) => void;
}
