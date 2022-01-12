export type Direction = 'right' | 'left' | 'top' | 'bottom';
export type LanguageType = 'javascript' | 'python' | 'xml' | 'markdown';

export interface Props {
  width: string;
  height: string;
  language: LanguageType;
  level: string;
  setCompleted: (completed: boolean) => void;
}
export interface ContainerProps {
  width: string;
  height: string;
}
