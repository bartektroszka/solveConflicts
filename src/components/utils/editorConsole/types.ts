import { Dispatch, SetStateAction } from "react";

export type Direction = "right" | "left" | "top" | "bottom";
export type LanguageType = "javascript" | "python" | "xml";

export interface Props {
  width: string;
  height: string;
  value: string;
  language: LanguageType;
  onChange: Dispatch<SetStateAction<string>>;
}
export interface ContainerProps {
  width: string;
  height: string;
}
