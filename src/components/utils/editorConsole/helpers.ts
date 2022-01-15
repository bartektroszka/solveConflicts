import { Node } from '../folderTree/types';

export const findNode = (node: Node, tree: Node[]) => {
  let foundArray = tree.filter((nd) => nd.id === node.id);
  let found;
  if (!foundArray.length) {
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
    found = foundArray[0];
  }
  if (!found) found = node;
  return found;
};
