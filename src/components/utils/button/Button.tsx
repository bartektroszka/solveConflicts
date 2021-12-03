import { $Button } from './Button.style';
import { Props } from './types';

export const Button = ({ onClick, width, height, buttonText }: Props) => {
  const DEFAULT_WIDTH = '11rem';
  const DEFAULT_HEIGHT = '2.2rem';

  return (
    <$Button
      width={width ?? DEFAULT_WIDTH}
      height={height ?? DEFAULT_HEIGHT}
      onClick={onClick}
    >
      {buttonText}
    </$Button>
  );
};
