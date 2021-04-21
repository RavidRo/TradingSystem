
import React ,{FC} from 'react';
import '../styles/PopupCart.scss';

type PopupCartProps = {
    content: string,
   
};
const PopupCart: FC<PopupCartProps> = ({content}: PopupCartProps) => {

	return (
		
		<div className="popupCart">
            <div className="box">
                <span className="close-icon"></span>
                {content}
            </div>
		</div>
	);
}

export default PopupCart;
