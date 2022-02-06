interface Popup {
  message: string;
  width: string;
  height: string;
  stage: number;
}

export interface Props {
  popups: Popup[];
  diplomaAvailable: boolean;
  levelNumber: number;
  setLevel: (levelNumber: number) => void;
  setCompletedLevels: (levels: number[]) => void;
  reset: (text: string) => void;
  task: string;
}
