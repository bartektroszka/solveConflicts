export interface Node {
  id: number;
  parentId: number | null;
  label: string;
  items?: Node[];
  data?: string;
  extension?: string;
}

export interface Props {
  data: Node[];
  setFile: (node: Node) => void;
}
