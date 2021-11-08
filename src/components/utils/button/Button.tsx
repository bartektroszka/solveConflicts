import { $Button } from "./Button.style"
import { Props } from "./types"


export const Button = ({ onClick, width, height } : Props) => {
    const DEFAULT_WIDTH = '150px'
    const DEFAULT_HEIGHT = '30px'

    return (
        <$Button width={width?? DEFAULT_WIDTH} height={height?? DEFAULT_HEIGHT} onClick={onClick}/>
    )
}