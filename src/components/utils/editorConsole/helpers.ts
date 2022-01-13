import { Node } from '../folderTree/types';

export const findNode = (node: Node, tree: Node[]) => {
  let found_array = tree.filter((nd) => nd.id === node.id);
  let found;
  if (!found_array.length) {
    tree.forEach((nd) => {
      if (nd.items) {
        nd.items.forEach((file) => {
          if (file.id === node.id) {
            found = file;
          }
        });
      }
    });
  } else {
    found = found_array[0];
  }
  if (!found) found = node;
  return found;
};
