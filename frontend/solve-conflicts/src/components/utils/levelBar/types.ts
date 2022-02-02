import { Size } from '../../../types';

export interface Props {
  numberOfLevels: number;
  currentLevel: number;
  availableLevels: number[];
  setLevel: (level:number) => void;
}
