import { $Button, $LoadingButton } from './Button.style';
import { Props } from './types';

export const Button = ({ onClick, width, height, buttonText, buttonLoadingText, loading }: Props) => {
  const DEFAULT_WIDTH = '11rem';
  const DEFAULT_HEIGHT = '2.2rem';
  

  return (
    loading? 
    <$LoadingButton
      width={width ?? DEFAULT_WIDTH}
      height={height ?? DEFAULT_HEIGHT}
      onClick={onClick}
    >
      {buttonLoadingText}
    </$LoadingButton>
    :
    <$Button
      width={width ?? DEFAULT_WIDTH}
      height={height ?? DEFAULT_HEIGHT}
      onClick={onClick}
    >
      {buttonText}
    </$Button>
  );
};
