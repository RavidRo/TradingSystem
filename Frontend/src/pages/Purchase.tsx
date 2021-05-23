import { Button, TextField } from '@material-ui/core';
import React, { FC, useState, useEffect, useRef } from 'react';
import '../styles/Purchase.scss';
import Timer from '../components/Timer';
import useAPI from '../hooks/useAPI';
import { useHistory } from 'react-router-dom';
import Swal from 'sweetalert2';

type PurchaseProps = {
	location: any;
};

const Purchase: FC<PurchaseProps> = ({ location }) => {
	const totalAmount = useRef<number>(
		location.state !== undefined ? location.state.totalAmount : 0
	);
	const [credit, setCredit] = useState<string>('');
	const [address, setAddress] = useState<string>('');
	// const [age,setAge] = useState<string>("");
	const history = useHistory();

	const handleUnload = (e: any) => {
		e.preventDefault();
	};

	useEffect(() => {
		window.addEventListener('beforeunload', handleUnload);
		return () => window.removeEventListener('beforeunload', handleUnload);
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [handleUnload]);

	const purchaseObj = useAPI<number>('/send_payment', {}, 'POST');
	const handlePurchase = () => {
		purchaseObj
			.request({
				cookie: location.state.cookie,
				payment_details: { credit },
				address: address,
			})
			.then(({ data, error }) => {
				if (!error && data !== null) {
					Swal.fire({
						icon: 'success',
						title: 'Congratulations!',
						text: data.data.toString(),
					});
				}
			});
	};
	const cancelObj = useAPI<number>('/cancel_purchase', {}, 'POST');
	const handleCancel = () => {
		cancelObj.request({ cookie: location.state.cookie }).then(({ data, error }) => {
			if (!error && data !== null) {
				// go back to cart
				history.goBack();
			}
		});
	};

	return (
		<div className='purchaseDiv'>
			<form noValidate autoComplete='on'>
				<div className='formDiv'>
					<TextField
						required
						id='standard-required'
						label='Credit Number'
						defaultValue=''
						style={{ width: '50%' }}
						onChange={(e) => setCredit(e.target.value)}
					/>
					<TextField
						required
						id='standard-required'
						label='Address'
						defaultValue=''
						style={{ marginTop: '5%', width: '50%' }}
						onChange={(e) => setAddress(e.target.value)}
					/>
				</div>
				<h3 className='totalPurchase'>Total amount : {totalAmount.current}</h3>
				<div className='buttonsDiv'>
					<Button
						className='cancelBtn'
						style={{
							background: '#AA0000',
							height: '50px',
							fontWeight: 'bold',
							fontSize: 'large',
							alignSelf: 'center',
							marginLeft: '40%',
						}}
						onClick={() => handleCancel()}
					>
						Cancel
					</Button>
					<Button
						className='purchaseBtn'
						style={{
							background: '#7FFF00',
							height: '50px',
							fontWeight: 'bold',
							fontSize: 'large',
							alignSelf: 'center',
							marginLeft: '5%',
						}}
						onClick={() => handlePurchase()}
					>
						Check
					</Button>
				</div>
				<Timer />
			</form>
		</div>
	);
};

export default Purchase;
