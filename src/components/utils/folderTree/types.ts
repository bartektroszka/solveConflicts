export interface Node {
  id: number;
  parentId: number | null;
  label: string;
  items?: FolderTreeData;
  data?: string;
}

export type FolderTreeData = Node[];

export interface Props {
  data: FolderTreeData;
  setFile: (node: Node) => void;
}
