import {
	Button,
	Dialog,
	DialogActions,
	DialogContent,
	DialogTitle,
	TableCell,
	TableRow,
	TextField,
} from '@material-ui/core';
import React, { FC, useContext, useState } from 'react';
import Swal from 'sweetalert2';
import useAPI from '../hooks/useAPI';
import { Offer } from '../types';
import { CookieContext, UsernameContext } from '../contexts';
import '../styles/OfferRow.scss';

type OffersRowProps = {
	offer: Offer;
	isManager: boolean;
};

const OffersRow: FC<OffersRowProps> = ({ offer, isManager }) => {
	const cookie = useContext(CookieContext);
	const username = useContext(UsernameContext);

	const [windowInput, setWindowInput] = useState<boolean>(false);
	const [offerInput, setOfferInput] = useState<number>(0);
	const [counterWindowInput, setCounterWindow] = useState<boolean>(false);
	const [counterInput, setCounterInput] = useState<number>(0);
	const [currentOffer, setCurrentOffer] = useState<Offer>(offer);

	// const offerStatus = ['undeclared', 'awaiting manager approval', 'counter offered', 'approved', 'rejected', 'cancled'];

	const handleDeclare = () => {
		setWindowInput(true);
	};
	const cancelOfferObj = useAPI<void>('/cancel_offer', {}, 'POST');
	const handleCancel = () => {
		cancelOfferObj.request({ offer_id: offer.id }).then(({ data, error }) => {
			if (!error && data) {
				Swal.fire({
					icon: 'success',
					title: 'Congratulations!',
					text: 'Your offer was canceled successfully!',
				});
				setCurrentOffer((offer) => {
					return {
						id: offer.id,
						price: offerInput,
						status: 'cancled',
						product_id: offer.product_id,
						product_name: offer.product_name,
						store_id: offer.store_id,
						store_name: offer.store_name,
						username: offer.username,
						awaiting_owners: [],
					};
				});
			}
		});
	};
	const declareOfferObj = useAPI<void>('/declare_price', {}, 'POST');
	const handleOK = () => {
		declareOfferObj
			.request({ cookie: cookie, offer_id: offer.id, price: offerInput })
			.then(({ data, error }) => {
				if (!error && data) {
					Swal.fire({
						icon: 'success',
						title: 'Congratulations!',
						text: 'Your offer was sent to the store manager, we will notify you when there will be an answer !',
					});
					setCurrentOffer((offer) => {
						return {
							id: offer.id,
							price: offerInput,
							status: 'awaiting manager approval',
							product_id: offer.product_id,
							product_name: offer.product_name,
							store_id: offer.store_id,
							store_name: offer.store_name,
							username: offer.username,
							awaiting_owners: [],
						};
					});
					setWindowInput(false);
				}
			});
	};
	const counterOfferObj = useAPI<void>('/suggest_counter_offer', {}, 'POST');
	const handleOKCounter = () => {
		setCounterWindow(false);
		counterOfferObj
			.request({
				cookie: cookie,
				store_id: offer.store_id,
				product_id: offer.product_id,
				offer_id: offer.id,
				price: counterInput,
			})
			.then(({ data, error }) => {
				if (!error && data !== null) {
					Swal.fire({
						icon: 'success',
						title: 'Congratulations!',
						text: 'Your counter offer was sent to the user, we will notify you when answer is received !',
					});
					setCurrentOffer((offer) => {
						return {
							id: offer.id,
							price: counterInput,
							status: 'awaiting manager approval',
							product_id: offer.product_id,
							product_name: offer.product_name,
							store_id: offer.store_id,
							store_name: offer.store_name,
							username: offer.username,
							awaiting_owners: [],
						};
					});
				}
			});
	};
	const acceptManagerOfferObj = useAPI<void>(
		'/approve_manager_offer',
		{ cookie: cookie, offer_id: offer.id },
		'POST'
	);
	const handleAccept = () => {
		acceptManagerOfferObj.request().then(({ data, error }) => {
			if (!error && data) {
				Swal.fire({
					icon: 'success',
					title: 'Congratulations!',
					text: 'The offered price on the item was approved, you can move the item to cart now !',
				});
			}
		});
	};
	const productObj = useAPI<void>('/save_product_in_cart', {}, 'POST');
	const handleMoveToCart = () => {
		productObj
			.request({
				cookie: cookie,
				store_id: offer.store_id,
				product_id: offer.product_id,
				quantity: 1,
			})
			.then(({ data, error }) => {
				if (!error && data !== null) {
					Swal.fire({
						icon: 'success',
						title: 'Congratulations!',
						text: 'The selected item was moved to the cart !',
					});
				}
			});
	};
	const approveUserObj = useAPI<void>(
		'/approve_user_offer',
		{
			cookie: cookie,
			store_id: offer.store_id,
			product_id: offer.product_id,
			offer_id: offer.id,
		},
		'POST'
	);
	const handleApprove = () => {
		approveUserObj.request().then(({ data, error }) => {
			const lastApproval = offer.awaiting_owners.length === 1;
			if (!error && data !== null) {
				Swal.fire({
					icon: 'success',
					title: 'Congratulations!',
					text: `You approved the selected item, ${
						lastApproval
							? 'message sent to user'
							: 'waiting for other managers to approve'
					} !`,
				});
				setCurrentOffer((offer) => {
					return {
						id: offer.id,
						price: offer.price,
						status: lastApproval ? 'approved' : offer.status,
						product_id: offer.product_id,
						product_name: offer.product_name,
						store_id: offer.store_id,
						store_name: offer.store_name,
						username: offer.username,
						awaiting_owners: offer.awaiting_owners.filter(
							(owner) => owner !== username
						),
					};
				});
			}
		});
	};
	const rejectUserObj = useAPI<void>(
		'/reject_user_offer',
		{
			cookie: cookie,
			store_id: offer.store_id,
			product_id: offer.product_id,
			offer_id: offer.id,
		},
		'POST'
	);
	const handleReject = () => {
		rejectUserObj.request().then(({ data, error }) => {
			if (!error && data !== null) {
				Swal.fire({
					icon: 'success',
					title: 'Congratulations!',
					text: 'The selected item was rejected, message sent to user !',
				});
				setCurrentOffer((offer) => {
					return {
						id: offer.id,
						price: counterInput,
						status: 'rejected',
						product_id: offer.product_id,
						product_name: offer.product_name,
						store_id: offer.store_id,
						store_name: offer.store_name,
						username: offer.username,
						awaiting_owners: [],
					};
				});
			}
		});
	};

	return (
		<TableRow key={offer.id}>
			<TableCell component='th' scope='row'>
				{currentOffer.product_name}
			</TableCell>
			<TableCell component='th' scope='row'>
				{currentOffer.store_name}
			</TableCell>
			<TableCell component='th' scope='row'>
				{currentOffer.price === null ? '---' : currentOffer.price}
			</TableCell>
			<TableCell component='th' scope='row'>
				{isManager && currentOffer.status === 'awaiting manager approval'
					? currentOffer.awaiting_owners.find((owner) => owner === username)
						? 'Awaiting for your approval'
						: 'Awaiting for others approval'
					: currentOffer.status}
			</TableCell>
			<TableCell component='th' scope='row'>
				{isManager === false ? (
					<button
						className='rowBtn'
						disabled={
							currentOffer.status !== 'undeclared' &&
							currentOffer.status !== 'counter offered'
						}
						onClick={handleDeclare}
					>
						Declare new price
					</button>
				) : (
					<button
						className='rowBtn'
						disabled={
							(currentOffer.status !== 'awaiting manager approval' &&
								currentOffer.status !== 'cancled') ||
							(currentOffer.status === 'awaiting manager approval' &&
								!currentOffer.awaiting_owners.find((owner) => owner === username))
						}
						onClick={handleApprove}
					>
						Approve
					</button>
				)}
			</TableCell>
			<TableCell component='th' scope='row'>
				{isManager === false ? (
					<button
						className='rowBtn'
						disabled={
							currentOffer.status === 'cancled' ||
							currentOffer.status === 'rejected' ||
							currentOffer.status === 'approved'
						}
						onClick={handleCancel}
					>
						Cancel Offer
					</button>
				) : (
					<button
						className='rowBtn'
						disabled={
							currentOffer.status !== 'awaiting manager approval' &&
							currentOffer.status !== 'cancled'
						}
						onClick={handleReject}
					>
						Reject
					</button>
				)}
			</TableCell>
			{isManager === false ? (
				<TableCell component='th' scope='row'>
					<button
						className='rowBtn'
						disabled={currentOffer.status !== 'counter offered'}
						onClick={handleAccept}
					>
						Accept Manager Offer
					</button>
				</TableCell>
			) : null}
			{isManager === false ? (
				<TableCell component='th' scope='row'>
					<button
						className='rowBtn'
						disabled={currentOffer.status !== 'approved'}
						onClick={handleMoveToCart}
					>
						Move To Cart
					</button>
				</TableCell>
			) : null}
			<TableCell component='th' scope='row'>
				{isManager === true ? (
					<button
						className='rowBtn'
						disabled={
							currentOffer.status !== 'counter offered' &&
							currentOffer.status !== 'awaiting manager approval'
						}
						onClick={() => setCounterWindow(true)}
					>
						Suggest Counter Offer
					</button>
				) : null}
			</TableCell>

			{/* for the first offer on an undeclared offer */}
			<Dialog
				open={windowInput}
				onClose={() => setWindowInput(false)}
				aria-labelledby='form-dialog-title'
			>
				<DialogTitle id='form-dialog-title'>Enter Your Offer</DialogTitle>
				<DialogContent>
					<TextField
						autoFocus
						margin='dense'
						id='offer'
						label='Offer'
						type='number'
						fullWidth
						onChange={(e) => setOfferInput(+e.target.value)}
					/>
				</DialogContent>
				<DialogActions>
					<Button style={{ color: 'blue' }} onClick={() => setWindowInput(false)}>
						Cancel
					</Button>
					<Button style={{ color: 'blue' }} onClick={() => handleOK()}>
						OK
					</Button>
				</DialogActions>
			</Dialog>
			{/* offer counter offer on existing offer */}
			<Dialog
				open={counterWindowInput}
				onClose={() => setCounterWindow(false)}
				aria-labelledby='form-dialog-title'
			>
				<DialogTitle id='form-dialog-title'>Enter Your Counter Offer</DialogTitle>
				<DialogContent>
					<TextField
						autoFocus
						margin='dense'
						id='offer'
						label='Offer'
						type='number'
						fullWidth
						onChange={(e) => setCounterInput(+e.target.value)}
					/>
				</DialogContent>
				<DialogActions>
					<Button style={{ color: 'blue' }} onClick={() => setCounterWindow(false)}>
						Cancel
					</Button>
					<Button style={{ color: 'blue' }} onClick={() => handleOKCounter()}>
						OK
					</Button>
				</DialogActions>
			</Dialog>
		</TableRow>
	);
};

export default OffersRow;
