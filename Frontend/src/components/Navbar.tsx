import React, { FC, useState,useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShoppingCart, faSignInAlt , faSearch} from '@fortawesome/free-solid-svg-icons';

import '../styles/Navbar.scss';
import config from '../config';
import PopupCart from '../components/PopupCart';

type NavBarProps = {
	 signedIn: boolean,
	 products:{id:string,name:string,price:number,quantity:number}[],
	 propHandleDelete:(product:{id:string,name:string,price:number})=>void,
	};

const Navbar: FC<NavBarProps> = ({ signedIn ,products,propHandleDelete}) => {
	const [hoverCart, setHoverCart] = useState<boolean>(false);
    const [productsInCart,setProducts] = useState<{id:string,name:string,price:number,quantity:number}[]>(products);

	useEffect(()=>{
        setProducts(products);
    },[products]);


	return (
		<div className="navbar">
			<nav>
				<Link className="nameLink" to="/">
					{config.website_name}!
				</Link>
				
				<div
					className="cartDiv"
					onMouseOver={() => setHoverCart(true)}
					onMouseLeave={() => setHoverCart(false)}
				>
					<FontAwesomeIcon className="cartIcon" icon={faShoppingCart} />
					<Link className="cartLink" to="/cart">
						My Cart
					</Link>
					{hoverCart ? <PopupCart products={productsInCart} propHandleDelete={propHandleDelete} /> : null}
				</div>
				<div className="storesDiv">
					<FontAwesomeIcon className="cartIcon" icon={faSearch} />
					<Link className="storesLink" to="/storesView">
						Stores
					</Link>
				</div>
				<div className="signInDiv">
					<FontAwesomeIcon className="signInIcon" icon={faSignInAlt} />
					{signedIn ? (
						<Link className="signInLink" to="/my-stores">
							Account&Stores
						</Link>
					) : (
						<Link className="signInLink" to="/sign-in">
							Sign In
						</Link>
					)}
				</div>
			</nav>
		</div>
	);
};

export default Navbar;
