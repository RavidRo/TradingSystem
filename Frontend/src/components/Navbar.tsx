import React, { FC, useState, useEffect, useContext } from 'react';

import {
	Badge,
	Button,
	ClickAwayListener,
	Divider,
	Fade,
	Grow,
	IconButton,
	List,
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
import { Product, ProductQuantity, StoreToSearchedProducts } from '../types';
import { AdminsContext, UsernameContext } from '../contexts';

type NavBarProps = {
	signedIn: boolean;
	products: ProductQuantity[];
	storesToProducts: StoreToSearchedProducts;
	propHandleDelete: (product: Product, storeID: string) => void;
	propHandleAdd: (product: Product, storeID: string) => void;
	notifications: string[];
	logout: () => void;
};

const Navbar: FC<NavBarProps> = ({
	signedIn,
	products,
	storesToProducts,
	propHandleDelete,
	notifications,
	propHandleAdd,
	logout,
}) => {
	const [hoverCart, setHoverCart] = useState<boolean>(false);
	const [productsInCart, setProducts] = useState<ProductQuantity[]>(products);
	const [openNotifications, setOpenNotifications] = useState<boolean>(false);
	const [accountMenuOpen, setAccountMenuOpen] = useState<boolean>(false);
	const accountMenuRef = React.useRef<HTMLButtonElement>(null);
	const history = useHistory();
	const username = useContext(UsernameContext);
	const admins = useContext(AdminsContext);

	useEffect(() => {
		setProducts(products);
	}, [products]);
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
					<Button className="item-link" onClick={() => history.push('/cart')}>
						<ShoppingCartIcon className="item-icon" />
						My Cart
					</Button>
					{hoverCart ? (
						<PopupCart
							products={productsInCart}
							storesToProducts={storesToProducts}
							propHandleAdd={propHandleAdd}
							propHandleDelete={propHandleDelete}
						/>
					) : null}
				</div>
				<div className="navbar-item">
					<Button className="item-link" onClick={() => history.push('/storesView')}>
						<SearchIcon className="item-icon" />
						Stores
					</Button>
				</div>
				<div className="navbar-item">
					{signedIn ? (
						<>
							{/* <FontAwesomeIcon className="item-icon" icon={faCaretDown} /> */}
							<Button
								ref={accountMenuRef}
								className="item-link"
								onClick={() => setAccountMenuOpen((prevOpen) => !prevOpen)}
							>
								<MoreVertIcon className="item-icon" />
								Account&Stores
							</Button>
						</>
					) : (
						<>
							<Button className="item-link" onClick={() => history.push('/sign-in')}>
								<ExitToAppIcon className="item-icon" />
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
											text="My stores"
											onClick={() => history.push('/my-stores')}
										>
											<StoreIcon />
										</AccountMenuItem>
										<AccountMenuItem
											text="My account"
											onClick={() => history.push('/my-account')}
										>
											<PersonIcon />
										</AccountMenuItem>
										{admins.includes(username) && (
											<AccountMenuItem
												text="Admin page"
												onClick={() => history.push('/admin')}
											>
												<SupervisorAccountIcon />
											</AccountMenuItem>
										)}
										<AccountMenuItem text="Logout" onClick={logout}>
											<MeetingRoomIcon />
										</AccountMenuItem>
									</MenuList>
								</ClickAwayListener>
							</Paper>
						</Grow>
					)}
				</Popper>
				<div className="navbar-item">
					<IconButton
						color={'inherit'}
						onClick={() => setOpenNotifications((open) => !open)}
					>
						<Badge badgeContent={notifications.length} color="primary">
							<NotificationsIcon className="item-icon" />
						</Badge>
					</IconButton>
					<Fade in={openNotifications}>
						<Paper className="notification-cont">
							<List component="ul">
								{notifications.map((notification, index) => (
									<>
										<ListItemText
											primary={notification}
											className="notification"
											key={index}
										/>
										<Divider key={index} />
									</>
								))}
							</List>
						</Paper>
					</Fade>
				</div>
			</nav>
		</div>
	);
};

export default Navbar;
