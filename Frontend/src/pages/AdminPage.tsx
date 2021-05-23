import React, { FC, useEffect, useState } from 'react';

import {
	Box,
	Container,
	createStyles,
	Divider,
	FormControl,
	IconButton,
	InputBase,
	InputLabel,
	makeStyles,
	MenuItem,
	Paper,
	Select,
	Theme,
	Typography,
} from '@material-ui/core';
import SearchIcon from '@material-ui/icons/Search';

import '../styles/AdminPage.scss';
import PurchaseHistoryTable from '../components/Lists/PurchaseHistoryTable';
import useAPI from '../hooks/useAPI';
import { PurchaseDetails, Store } from '../types';

const useStyles = makeStyles((theme: Theme) =>
	createStyles({
		searchForm: {
			padding: '2px 4px 10px',
			display: 'flex',
			alignItems: 'center',
		},
		header: {
			marginRight: 10,
		},
		input: {
			marginLeft: theme.spacing(1),
			flex: 1,
		},
		iconButton: {
			padding: 10,
		},
		divider: {
			height: 28,
			margin: 4,
		},
	})
);

type AdminPageProps = {};

type SearchBy = 'username' | 'store';
const AdminPage: FC<AdminPageProps> = () => {
	const { request: requestStoreHistory } = useAPI<PurchaseDetails[]>(
		'/get_any_store_purchase_history'
	);
	const { request: requestUserHistory } = useAPI<PurchaseDetails[]>('/get_user_purchase_history');
	const { request: requestStores } = useAPI<Store[]>('/get_stores_details');

	const [purchaseHistory, setPurchaseHistory] = useState<PurchaseDetails[]>([]);
	const [searchBy, setSearchBy] = useState<SearchBy>('username');
	const [search, setSearch] = useState<string>('');
	const [stores, setStores] = useState<Store[]>([]);
	const [selectedStore, setSelectedStore] = useState<string>('');

	useEffect(() => {
		requestStores({}, (data, error) => {
			if (!error && data) {
				setStores(data.data);
			}
		});
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const handleSearchChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setSearchBy(event.target.value as SearchBy);
	};
	const handleSelectedStoreChange = (event: React.ChangeEvent<{ value: unknown }>) => {
		setSelectedStore(event.target.value as string);
	};

	const onSubmit = (event: React.FormEvent<HTMLElement>) => {
		console.log(event);
		const request = searchBy === 'username' ? requestUserHistory : requestStoreHistory;
		const params = searchBy === 'username' ? { username: search } : { store_id: selectedStore };
		request(params, (data, error) => {
			if (!error && data) {
				setPurchaseHistory(data.data);
			}
		});
		event.preventDefault();
	};

	const classes = useStyles();
	return (
		<Container className="account-page-cont">
			<Paper className="history-cont">
				<Box component="form" className={classes.searchForm} onSubmit={onSubmit}>
					<Typography className={classes.header} gutterBottom>
						Purchase History
					</Typography>
					<Divider className={classes.divider} orientation="vertical" />
					{searchBy === 'username' ? (
						<InputBase
							className={classes.input}
							placeholder="Search by user"
							onChange={(event) => setSearch(event.currentTarget.value)}
						/>
					) : (
						<FormControl className={classes.input}>
							<InputLabel id="stores-label">Search By Store</InputLabel>
							<Select
								labelId="search-by-label"
								id="search-by-select"
								value={selectedStore}
								onChange={handleSelectedStoreChange}
							>
								{stores.map((store) => (
									<MenuItem value={store.id}>{store.name}</MenuItem>
								))}
							</Select>
						</FormControl>
					)}
					<IconButton type="submit" className={classes.iconButton} aria-label="search">
						<SearchIcon />
					</IconButton>
					<Divider className={classes.divider} orientation="vertical" />
					<FormControl className={classes.input}>
						<InputLabel id="search-by-label">Search By</InputLabel>
						<Select
							labelId="search-by-label"
							id="search-by-select"
							value={searchBy}
							onChange={handleSearchChange}
						>
							<MenuItem value="username">User</MenuItem>
							<MenuItem value="store">Store</MenuItem>
						</Select>
					</FormControl>
				</Box>

				<PurchaseHistoryTable history={purchaseHistory} />
			</Paper>
		</Container>
	);
};

export default AdminPage;
