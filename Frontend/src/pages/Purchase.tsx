import React, { FC, useState, useEffect, useRef } from 'react';

import { useHistory } from 'react-router-dom';

import { DatePicker } from '@material-ui/pickers';
import { Button, TextField } from '@material-ui/core';

import '../styles/Purchase.scss';
import Timer from '../components/Timer';
import { useAPI2 } from '../hooks/useAPI';
import { cancelPurchase, sendPayment } from '../api';
import { confirmOnSuccess } from '../decorators';

type MyTextFieldProps = {
	name: string;
	setValue: (newValue: string) => void;
	width?: string;
	numeric?: boolean;
};
const MyTextField: FC<MyTextFieldProps> = ({ name, setValue, width = '20%', numeric = false }) => {
	return (
		<TextField
			required
			id={name}
			label={name}
			defaultValue=''
			className='text-field'
			style={{ width }}
			onChange={(e) => setValue(e.target.value)}
			{...(numeric ? { inputMode: 'numeric', type: 'number' } : {})}
		/>
	);
};

type PurchaseProps = {
	location: any;
};

const Purchase: FC<PurchaseProps> = ({ location }) => {
	const totalAmount = useRef<number>(
		location.state !== undefined ? location.state.totalAmount : 0
	);

	// address: name, address, city, country, zip
	// purchase_details: card_number, month, year, holder, ccv, id

	// Address
	const [name, setName] = useState<string>('');
	const [address, setAddress] = useState<string>('');
	const [city, setCity] = useState<string>('');
	const [country, setCountry] = useState<string>('');
	const [zip, setZip] = useState<string>('');

	// Payment
	const [cardNumber, setCardNumber] = useState<string>('');
	const [holderName, setHolderName] = useState<string>('');
	const [ccv, setCcv] = useState<string>('');
	const [id, setId] = useState<string>('');
	const [expiringDate, setExpiringDate] = useState(new Date());

	const history = useHistory();

	useEffect(() => {
		const handleUnload = (e: any) => {
			e.preventDefault();
		};
		window.addEventListener('beforeunload', handleUnload);
		return () => window.removeEventListener('beforeunload', handleUnload);
	}, []);

	const purchaseAPI = useAPI2(sendPayment);
	const handlePurchase = confirmOnSuccess(
		() =>
			purchaseAPI.request(
				{
					card_number: cardNumber,
					holder: holderName,
					ccv: ccv,
					id,
					month: expiringDate.getMonth(),
					year: expiringDate.getFullYear(),
				},
				{ name, address, city, country, zip }
			),
		'Congratulations!'
	);

	const cancelAPI = useAPI2(cancelPurchase);
	const handleCancel = () => {
		cancelAPI.request().then(() => history.goBack());
	};

	return (
		<div className='purchaseDiv'>
			<form noValidate autoComplete='on'>
				<div className='formDiv-container'>
					<div className='formDiv'>
						<h3 className='section-title'>Shipping Details</h3>
						<MyTextField name='Name' setValue={setName} width='40%' />
						<MyTextField name='Address' setValue={setAddress} width='40%' />
						<MyTextField name='City' setValue={setCity} />
						<MyTextField name='Country' setValue={setCountry} />
						<MyTextField name='ZIP' setValue={setZip} width='10%' numeric />

						<h3 className='section-title'>Payment Details</h3>
						<MyTextField
							name='Card Number'
							setValue={setCardNumber}
							width='30%'
							numeric
						/>
						<MyTextField name='CCV' setValue={setCcv} width='30%' numeric />
						<DatePicker
							variant='inline'
							openTo='year'
							views={['year', 'month']}
							label='Expiring Date'
							value={expiringDate}
							onChange={(date) => setExpiringDate(date as Date)}
							className='text-field'
							style={{ width: '20%' }}
						/>
						<MyTextField name='Card holder Name' setValue={setHolderName} />
						<MyTextField name='Card holder ID' setValue={setId} numeric />
					</div>
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
						onClick={() => handlePurchase().then(() => history.push('/'))}
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
