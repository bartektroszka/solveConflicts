export interface Props {
  icon: "task" | "diploma";
  buttonText: string;
  onClick: () => void;
  width: string;
  height: string;
  active: boolean;
}
