
import { AppBar, IconButton, Toolbar, Typography } from '@material-ui/core';
import React ,{FC, useState} from 'react';
import { BrowserRouter, Switch, Route, Link } from 'react-router-dom';
import '../styles/Navbar.scss';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faShoppingCart } from '@fortawesome/free-solid-svg-icons';
import {faSignInAlt}from '@fortawesome/free-solid-svg-icons';
import PopupCart from './PopupCart';

type NavBarProps = {};
const Navbar: FC<NavBarProps> = () => {

	const [hoverCart, setHoverCart] = useState<boolean>(false);

	return (

		
		<div className="navbar">
			<nav>
			<Link className="nameLink" to='/'>Shopping World!</Link>
			<div className="cartDiv"
				onMouseOver={()=>setHoverCart(true)}
				onMouseLeave={()=>setHoverCart(false)}
			>
				<FontAwesomeIcon className="cartIcon" icon={faShoppingCart} />
				<Link className="cartLink" to='/'>My Cart</Link>
				{hoverCart?
				<PopupCart
					content={"your cart is:"}
				>
				</PopupCart>
				: null}
			</div>
			<div className="signInDiv">
				<FontAwesomeIcon className="signInIcon" icon={faSignInAlt} />
				<Link className="signInLink" to='/'>Sign In</Link>
			</div>
			</nav>
		</div>
	);
}

export default Navbar;
