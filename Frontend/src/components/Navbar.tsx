import React, { FC, useState, useEffect, useContext } from 'react';

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
import BarChartAdminIcon from '@material-ui/icons/BarChart';
import PersonIcon from '@material-ui/icons/Person';
import MoreVertIcon from '@material-ui/icons/MoreVert';
import SearchIcon from '@material-ui/icons/Search';
import ShoppingCartIcon from '@material-ui/icons/ShoppingCart';
import MeetingRoomIcon from '@material-ui/icons/MeetingRoom';
import NotificationsIcon from '@material-ui/icons/Notifications';

import { Link, useHistory } from 'react-router-dom';

import '../styles/Navbar.scss';
import config from '../config';
import PopupCart from '../components/PopupCart';
import { Product, StoreToSearchedProducts, notificationTime } from '../types';
import { AdminsContext, UsernameContext } from '../contexts';

type NavBarProps = {
	signedIn: boolean;
	storesToProducts: StoreToSearchedProducts;
	propHandleDelete: (product: Product, storeID: string) => Promise<boolean> | boolean;
	notifications: notificationTime[];
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
	const [accountMenuOpen, setAccountMenuOpen] = useState<boolean>(false);
	const accountMenuRef = React.useRef<HTMLButtonElement>(null);
	const history = useHistory();
	const username = useContext(UsernameContext);
	const admins = useContext(AdminsContext);

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
					<Button className='item-link' onClick={() => history.push('/cart')}>
						<ShoppingCartIcon className='item-icon' />
						My Cart
					</Button>
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
					<Button className='item-link' onClick={() => history.push('/storesView')}>
						<SearchIcon className='item-icon' />
						Stores
					</Button>
				</div>
				<div className='navbar-item'>
					{signedIn ? (
						<>
							<Button
								ref={accountMenuRef}
								className='item-link'
								onClick={() => setAccountMenuOpen((prevOpen) => !prevOpen)}
							>
								<MoreVertIcon className='item-icon' />
								Account&Stores
							</Button>
						</>
					) : (
						<>
							<Button className='item-link' onClick={() => history.push('/sign-in')}>
								<ExitToAppIcon className='item-icon' />
								Sign In
							</Button>
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
											<PersonIcon />
										</AccountMenuItem>
										{admins.includes(username) && (
											<AccountMenuItem
												text='Admin page'
												onClick={() => history.push('/admin')}
											>
												<SupervisorAccountIcon />
											</AccountMenuItem>
										)}
										{admins.includes(username) && (
											<AccountMenuItem
												text='View Statistics'
												onClick={() => history.push('/statistics')}
											>
												<BarChartAdminIcon />
											</AccountMenuItem>
										)}
										<AccountMenuItem text='Logout' onClick={logout}>
											<MeetingRoomIcon />
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
								notifications: notifications,
								// update: ()=>console.log("hi Ravid")
							},
						}}
					>
						<IconButton color={'inherit'}>
							<Badge badgeContent={notifications.length} showZero color='primary'>
								<NotificationsIcon className='item-icon'/>
							</Badge>
						</IconButton>
					</Link>
				</div>
			</nav>
		</div>
	);
};

export default Navbar;
