import { $Button, $HighlightedButton, $LoadingButton } from './Button.style';
import { Props } from './types';

export const Button = ({
  onClick,
  width,
  height,
  buttonText,
  buttonLoadingText,
  loading,
  highlighted,
}: Props) => {
  const DEFAULT_WIDTH = '11rem';
  const DEFAULT_HEIGHT = '2.2rem';

  const returnButton = () => {
    if (loading) {
      return (
        <$LoadingButton
          width={width ?? DEFAULT_WIDTH}
          height={height ?? DEFAULT_HEIGHT}
          onClick={onClick}
        >
          {buttonLoadingText}
        </$LoadingButton>
      );
    } else if (highlighted) {
      return (
        <$HighlightedButton
          width={width ?? DEFAULT_WIDTH}
          height={height ?? DEFAULT_HEIGHT}
          onClick={onClick}
        >
          {buttonText}
        </$HighlightedButton>
      );
    } else {
      return (
        <$Button
          width={width ?? DEFAULT_WIDTH}
          height={height ?? DEFAULT_HEIGHT}
          onClick={onClick}
        >
          {buttonText}
        </$Button>
      );
    }
  };

  return returnButton();
};
