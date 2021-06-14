import React, { FC } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Box from '@material-ui/core/Box';
import Collapse from '@material-ui/core/Collapse';
import IconButton from '@material-ui/core/IconButton';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import KeyboardArrowDownIcon from '@material-ui/icons/KeyboardArrowDown';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import { PurchaseDetails } from '../../types';

const useRowStyles = makeStyles({
	root: {
		'& > *': {
			borderBottom: 'unset',
		},
	},
});

const Row: FC<{ row: PurchaseDetails; showUsername: boolean }> = (props) => {
	const { row, showUsername } = props;
	const [open, setOpen] = React.useState(false);
	const classes = useRowStyles();

	return (
		<>
			<TableRow className={classes.root} onClick={() => setOpen(!open)}>
				<TableCell>
					<IconButton aria-label='expand row' size='small' onClick={() => setOpen(!open)}>
						{open ? <KeyboardArrowUpIcon /> : <KeyboardArrowDownIcon />}
					</IconButton>
				</TableCell>
				<TableCell component='th' scope='row'>
					{new Date(row.date).toDateString()}
				</TableCell>
				<TableCell>{showUsername ? row.username : row.store_name}</TableCell>
				<TableCell align='right'>{row.total_price}</TableCell>
			</TableRow>
			<TableRow>
				<TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={6}>
					<Collapse in={open} timeout='auto' unmountOnExit>
						<Box margin={1}>
							{/* <Typography variant="h6" gutterBottom component="div">
								Products
							</Typography> */}
							<Table size='small' aria-label='purchases'>
								<TableHead>
									<TableRow>
										<TableCell>Product Name</TableCell>
									</TableRow>
								</TableHead>
								<TableBody>
									{row.product_names.map((product_name) => (
										<TableRow key={product_name}>
											<TableCell component='th' scope='row'>
												{product_name}
											</TableCell>
										</TableRow>
									))}
								</TableBody>
							</Table>
						</Box>
					</Collapse>
				</TableCell>
			</TableRow>
		</>
	);
};

const PurchaseHistoryTable: FC<{ history: PurchaseDetails[]; showUsername?: boolean }> = ({
	history,
	showUsername = false,
}) => {
	return (
		<TableContainer component={Paper}>
			<Table aria-label='purchase history table' stickyHeader>
				<TableHead>
					<TableRow>
						<TableCell />
						<TableCell>Date</TableCell>
						<TableCell>{`${showUsername ? 'Username' : 'Store'}`}</TableCell>
						<TableCell align='right'>Price</TableCell>
					</TableRow>
				</TableHead>
				<TableBody>
					{history.map((row, index) => (
						<Row key={index} row={row} showUsername={showUsername} />
					))}
				</TableBody>
			</Table>
		</TableContainer>
	);
};

export default PurchaseHistoryTable;
