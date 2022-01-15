import Tree, { NodeId } from '@naisutech/react-tree';
import { Props, Node } from './types';

const FolderTree = ({ data, setFile }: Props) => {
  const findNodeById = (id: number, data: Node[]): Node | null => {
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
        if (node) setFile(node);
      }}
      containerStyle={{ width: '30%' }}
      nodes={data}
    />
  );
};

export default FolderTree;
