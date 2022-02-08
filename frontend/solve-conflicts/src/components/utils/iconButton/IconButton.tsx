import { reduceEachLeadingCommentRange } from 'typescript';
import { $IconButton, $IconButtonDisabled } from './IconButton.style';
import { Props } from './types';

export const IconButton = ({
  icon,
  buttonText,
  onClick,
  width,
  height,
  active,
}: Props) => {
  const returnIcon = () => {
    if (icon === 'diploma') {
      return (
        <img
          src={window.location.origin + '/diploma-white.png'}
          width='23px'
          height='16px'
          style={{ color: 'red' }}
        />
      );
    } else if (icon === 'task') {
      return (
        <img
          src={window.location.origin + '/task-white.png'}
          width='25px'
          height='22px'
          style={{ color: 'red' }}
        />
      );
    }
  };
  return (
    <>
      {active ? (
        <$IconButton width={width} height={height} onClick={onClick}>
          {returnIcon()}
          {buttonText}
        </$IconButton>
      ) : (
        <$IconButtonDisabled width={width} height={height} onClick={() => {}}>
          {returnIcon()}
          {buttonText}
        </$IconButtonDisabled>
      )}
    </>
  );
};
