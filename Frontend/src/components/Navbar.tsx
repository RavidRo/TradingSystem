import React, { FC, useState } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShoppingCart, faSignInAlt } from '@fortawesome/free-solid-svg-icons';

import '../styles/Navbar.scss';
import config from '../config';
import PopupCart from '../components/PopupCart';

type NavBarProps = { signedIn: boolean };
const Navbar: FC<NavBarProps> = ({ signedIn }) => {
	const [hoverCart, setHoverCart] = useState<boolean>(false);

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
					{hoverCart ? <PopupCart content={'your cart is:'} /> : null}
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
