export interface Props {
  width: string;
  height: string;
  children: React.ReactNode;
  open: boolean;
  afterClose: () => void;
  buttonText: string;
}
