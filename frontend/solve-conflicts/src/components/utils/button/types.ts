export interface Props {
  width?: string;
  height?: string;
  buttonText: string;
  buttonLoadingText?: string;
  loading?: boolean;
  onClick: () => void;
  highlighted?: boolean;
}
