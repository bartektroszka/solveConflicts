export interface Props {
  setLevel: (levelNumber: number) => void;
  setAvailableLevels: (levels: number[]) => void;
  reset: (text: string) => void;
}
