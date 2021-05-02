import React, { FC, useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
	faShoppingCart,
	faSignInAlt,
	faSearch,
	faBell,
	faSignOutAlt,
} from '@fortawesome/free-solid-svg-icons';

import '../styles/Navbar.scss';
import config from '../config';
import PopupCart from '../components/PopupCart';
import { Product } from '../types';
import { Badge, Divider, IconButton, List, ListItemText } from '@material-ui/core';

type NavBarProps = {
	signedIn: boolean;
	products: Product[];
	propHandleDelete: (product: Product) => void;
	notification: string[];
	logout: () => void;
};

const Navbar: FC<NavBarProps> = ({
	signedIn,
	products,
	propHandleDelete,
	notification,
	logout,
}) => {
	const [hoverCart, setHoverCart] = useState<boolean>(false);
	const [productsInCart, setProducts] = useState<Product[]>(products);

	useEffect(() => {
		setProducts(products);
	}, [products]);

	return (
		<div className="navbar">
			<nav>
				<Link className="nameLink" to="/">
					{config.website_name}!
				</Link>

				<div
					className="navbar-item"
					onMouseOver={() => setHoverCart(true)}
					onMouseLeave={() => setHoverCart(false)}
				>
					<FontAwesomeIcon className="item-icon" icon={faShoppingCart} />
					<Link className="item-link" to="/cart">
						My Cart
					</Link>
					{hoverCart ? (
						<PopupCart products={productsInCart} propHandleDelete={propHandleDelete} />
					) : null}
				</div>
				<div className="navbar-item">
					<FontAwesomeIcon className="item-icon" icon={faSearch} />
					<Link className="item-link" to="/storesView">
						Stores
					</Link>
				</div>
				{signedIn && (
					<div className="navbar-item">
						<FontAwesomeIcon className="item-icon" icon={faSignOutAlt} />
						<Link className="item-link" to="/" onClick={() => logout()}>
							Logout
						</Link>
					</div>
				)}
				<div className="navbar-item">
					<FontAwesomeIcon className="item-icon" icon={faSignInAlt} />
					{signedIn ? (
						<Link className="item-link" to="/my-stores">
							Account&Stores
						</Link>
					) : (
						<Link className="item-link" to="/sign-in">
							Sign In
						</Link>
					)}
				</div>
				<div className="navbar-item">
					<IconButton color={'inherit'}>
						<Badge badgeContent={notification.length} showZero color="primary">
							<FontAwesomeIcon className="item-icon" icon={faBell} />
						</Badge>
					</IconButton>
					{/* <List component="ul" style={{ position: 'absolute', padding-top: 50 }}>
						<ListItemText primary="Inbox" />
						<Divider />
						<ListItemText primary="Drafts" />
					</List> */}
				</div>
			</nav>
		</div>
	);
};

export default Navbar;
