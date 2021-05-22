import React, { FC, useState, useEffect } from 'react';

import {
	Badge,
	Button,
	ClickAwayListener,
	Grow,
	IconButton,
	ListItemIcon,
	ListItemText,
	MenuItem,
	MenuList,
	Paper,
	Popper,
} from '@material-ui/core';
import ExitToAppIcon from '@material-ui/icons/ExitToApp';
import StoreIcon from '@material-ui/icons/Store';
import SupervisorAccountIcon from '@material-ui/icons/SupervisorAccount';

import { Link, useHistory } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
	faShoppingCart,
	faSignInAlt,
	faSearch,
	faBell,
	faCaretDown,
} from '@fortawesome/free-solid-svg-icons';

import '../styles/Navbar.scss';
import config from '../config';
import PopupCart from '../components/PopupCart';
import { Product, StoreToSearchedProducts } from '../types';

type NavBarProps = {
	signedIn: boolean;
	storesToProducts: StoreToSearchedProducts;
	propHandleDelete: (product: Product, storeID: string) => Promise<boolean> | boolean;
	notifications: string[];
	changeQuantity: (store: string, product: string, quantity: number) => Promise<boolean>;
	logout: () => void;
	propUpdateStores: (map: StoreToSearchedProducts) => void;
};

const Navbar: FC<NavBarProps> = ({
	signedIn,
	storesToProducts,
	propHandleDelete,
	notifications,
	changeQuantity,
	logout,
	propUpdateStores,
}) => {
	const [hoverCart, setHoverCart] = useState<boolean>(false);
	const [storesToProductsMy, setStoresProducts] =
		useState<StoreToSearchedProducts>(storesToProducts);
	const [myNotifications, setNotifications] = useState<string[]>(notifications);
	const [accountMenuOpen, setAccountMenuOpen] = useState<boolean>(false);
	const accountMenuRef = React.useRef<HTMLButtonElement>(null);
	const history = useHistory();

	useEffect(() => {
		setNotifications((old) => [...old, ...notifications]);
	}, [notifications]);
	useEffect(() => {
		setStoresProducts(storesToProducts);
	}, [storesToProducts]);

	const handleCloseMenu = () => setAccountMenuOpen(false);

	const AccountMenuItem: FC<{ onClick?: () => void; text: string }> = ({
		onClick,
		text,
		children,
	}) => {
		return (
			<MenuItem
				onClick={() => {
					handleCloseMenu();
					onClick && onClick();
				}}
			>
				{children && <ListItemIcon>{children}</ListItemIcon>}
				<ListItemText primary={text} />
			</MenuItem>
		);
	};

	return (
		<div className='navbar'>
			<nav>
				<Link className='nameLink' to='/'>
					{config.website_name}!
				</Link>

				<div
					className='navbar-item'
					onMouseOver={() => setHoverCart(true)}
					onMouseLeave={() => setHoverCart(false)}
				>
					<FontAwesomeIcon className='item-icon' icon={faShoppingCart} />
					<Link className='item-link' to='/cart'>
						My Cart
					</Link>
					{hoverCart ? (
						<PopupCart
							storesToProducts={storesToProductsMy}
							propHandleDelete={propHandleDelete}
							changeQuantity={changeQuantity}
							propUpdateStores={propUpdateStores}
						/>
					) : null}
				</div>
				<div className='navbar-item'>
					<FontAwesomeIcon className='item-icon' icon={faSearch} />
					<Link className='item-link' to='/storesView'>
						Stores
					</Link>
				</div>
				<div className='navbar-item'>
					{signedIn ? (
						<>
							<FontAwesomeIcon className='item-icon' icon={faCaretDown} />
							<Button
								ref={accountMenuRef}
								className='item-link'
								onClick={() => setAccountMenuOpen((prevOpen) => !prevOpen)}
							>
								Account&Stores
							</Button>
						</>
					) : (
						<>
							<FontAwesomeIcon className='item-icon' icon={faSignInAlt} />
							<Link className='item-link' to='/sign-in'>
								Sign In
							</Link>
						</>
					)}
				</div>
				<Popper
					open={accountMenuOpen}
					anchorEl={accountMenuRef.current}
					transition
					// disablePortal
				>
					{({ TransitionProps }) => (
						<Grow {...TransitionProps}>
							<Paper>
								<ClickAwayListener onClickAway={handleCloseMenu}>
									<MenuList autoFocusItem={accountMenuOpen} onKeyDown={() => {}}>
										<AccountMenuItem
											text='My stores'
											onClick={() => history.push('/my-stores')}
										>
											<StoreIcon />
										</AccountMenuItem>
										<AccountMenuItem
											text='My account'
											onClick={() => history.push('/my-account')}
										>
											<SupervisorAccountIcon />
										</AccountMenuItem>
										<AccountMenuItem text='Logout' onClick={logout}>
											<ExitToAppIcon />
										</AccountMenuItem>
									</MenuList>
								</ClickAwayListener>
							</Paper>
						</Grow>
					)}
				</Popper>
				<div className='navbar-item'>
					<Link
						className='item-link'
						to={{
							pathname: '/Notifications',
							state: {
								notifications: myNotifications,
							},
						}}
					>
						<IconButton color={'inherit'}>
							<Badge badgeContent={myNotifications.length} showZero color='primary'>
								<FontAwesomeIcon className='item-icon' icon={faBell} />
							</Badge>
						</IconButton>
					</Link>
				</div>
			</nav>
		</div>
	);
};

export default Navbar;
