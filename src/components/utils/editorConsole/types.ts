export type Direction = "right" | "left" | "top" | "bottom";
export type LanguageType = "javascript" | "python" | "xml" | "markdown";

export interface Props {
  width: string;
  height: string;
  levelNumber: number;

  executionResponseCallback: (response: any) => void;
}
export interface ContainerProps {
  width: string;
  height: string;
}
