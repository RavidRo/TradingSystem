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
import { Product, ProductQuantity, StoreToSearchedProducts } from '../types';
import { Badge, IconButton} from '@material-ui/core';

type NavBarProps = {
	signedIn: boolean;
	products: ProductQuantity[];
	storesToProducts: StoreToSearchedProducts;
	propHandleDelete: (product: Product, storeID: string) => Promise<boolean> | boolean;
	notifications: string[];
	changeQuantity:(store:string,product:string,quan:number)=>Promise<boolean>;
	logout: () => void;
	propUpdateStores:(map:StoreToSearchedProducts)=>void,
};

const Navbar: FC<NavBarProps> = ({signedIn,products,storesToProducts,propHandleDelete,notifications,changeQuantity,logout,propUpdateStores}) => {
	const [hoverCart, setHoverCart] = useState<boolean>(false);
	const [productsInCart, setProducts] = useState<ProductQuantity[]>(products);
const [openNotifications, setOpenNotifications] = useState<boolean>(false);
    const [storesToProductsMy,setStoresProducts] = useState<StoreToSearchedProducts>(storesToProducts);
	const [myNotifications, setNotifications] = useState<string[]>(notifications);

	useEffect(()=>{
		// TODO: change to what got from props
		setNotifications(notifications);
		console.log(notifications);
	},[notifications]);


	useEffect(()=>{
		setStoresProducts(storesToProducts);
	},[storesToProducts]);


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
						<PopupCart
							products={productsInCart}
							storesToProducts={storesToProductsMy}
							propHandleDelete={propHandleDelete}
							changeQuantity={changeQuantity}
							propUpdateStores={propUpdateStores}
						/>
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
					<Link 
						className="item-link" 
						to={{
                            pathname: '/Notifications',
                            state: {
                                notifications: myNotifications
                            },
                            }}
					>
						<IconButton color={'inherit'}>
							<Badge badgeContent={myNotifications.length} showZero color="primary">
								<FontAwesomeIcon className="item-icon" icon={faBell} />
							</Badge>
						</IconButton>
					</Link>
				</div>
			</nav>
		</div>
	);
};

export default Navbar;
