import styled from 'styled-components';
import { Size } from 'src/types';

export const $FolderTree = styled.div<Size>`
  width: ${(props) => props.width};
  height: ${(props) => props.height};
  border: 1px solid #000;
  justify-content: center;
`;
