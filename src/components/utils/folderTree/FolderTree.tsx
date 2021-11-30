import Tree, { NodeId } from '@naisutech/react-tree';
import { FolderTreeData, Props, Node } from './types';

const FolderTree = ({ data, setFile }: Props) => {
  const findNodeById = (id: number, data: FolderTreeData): Node | null => {
    for (let i = 0; i < data.length; i++) {
      const child = data[i];
      if (child.id === id) return child;
      if (child.items) {
        const searchChild = findNodeById(id, child.items);
        if (searchChild) return searchChild;
      }
    }
    return null;
  };

  return (
    <Tree
      size={'narrow'}
      onSelect={(nodeIds: NodeId[]) => {
        const node = findNodeById(nodeIds[0] as number, data);
        if (node?.data) setFile(node);
      }}
      containerStyle={{ width: '20%' }}
      nodes={data}
    />
  );
};

export default FolderTree;
