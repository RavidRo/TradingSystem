import React, { FC, useEffect, useState } from 'react';

import { Appointee, Product, Store, ProductQuantity } from '../types';
import AppointeeDetails from './DetailsWindows/AppointeeDetails';
import useAPI from '../hooks/useAPI';
import ProductsList from './Lists/ProductsList';
import MyAppointeesList from './Lists/MyAppointeesList';
import AppointeesList from './Lists/AppointeesList';
import DiscountsList from './Lists/DiscountsList';
import ConditionsList from './Lists/ConditionsList';
import StorePurchaseHistory from './Lists/StorePurchaseHistory';
import OffersTable from './OffersTable';
import '../styles/ManageStore.scss';

type ManageStoreProps = {
	storeId: string;
	appointment: Appointee;
	setAppointment: (storeId: string, appointment: Appointee) => void;
};

const ManageStore: FC<ManageStoreProps> = ({ storeId, appointment, setAppointment }) => {
	const [products, setProducts] = useState<ProductQuantity[]>([]);
	const [store, setStore] = useState<Store | null>(null);

	const getProductsByStore = useAPI<Product[]>('/get_products_by_store', {
		store_id: storeId,
	});

	const getStore = useAPI<Store>('/get_store', {
		store_id: storeId,
	});

	useEffect(() => {
		Promise.all([getProductsByStore.request(), getStore.request()]).then(
			([getProductsByStore, getStore]) => {
				if (
					!getProductsByStore.error &&
					getProductsByStore.data !== null &&
					!getStore.error &&
					getStore.data !== null
				) {
					setStore(getStore.data.data);
					setProducts(
						getProductsByStore.data.data.map((product) => ({
							...product,
							quantity: (getStore.data?.data as Store).ids_to_quantities[product.id],
						}))
					);
				}
			}
		);
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, []);

	const [selectedItem, setSelectedItem] = useState<string>('');
	const [open, setOpen] = useState<boolean>(false);
	const [Tab, setTab] = useState<FC | null>(null);

	useEffect(() => {
		setOpen(false);
	}, [products]);

	const setTabAnimation = (component: FC) => {
		setOpen(false);
		setTimeout(() => {
			setTab(() => component);
			setOpen(true);
		}, 300);
	};

	const openTab = (component: FC, selectedItem: string) => {
		setSelectedItem(selectedItem);
		setTabAnimation(component);
	};

	const onSelectAppointee = (appointee: Appointee) => {
		if (appointee.username !== selectedItem) {
			openTab(() => <AppointeeDetails appointee={appointee} />, appointee.username);
		}
	};

	return (
		<div className='my-store-page'>
			<div className='my-store-cont'>
				{store && (
					<>
						{appointment.permissions.includes('manage products') && (
							<ProductsList
								openTab={openTab}
								products={products}
								selectedItem={selectedItem}
								setProducts={setProducts}
								storeId={store.id}
							/>
						)}
						<MyAppointeesList
							onSelectAppointee={onSelectAppointee}
							openTab={openTab}
							selectedItem={selectedItem}
							storeId={store.id}
							store_name={store.name}
							appointment={appointment}
							setAppointment={setAppointment}
						/>
						{appointment.permissions.includes('get appointments') && (
							<AppointeesList
								onSelectAppointee={onSelectAppointee}
								selectedItem={selectedItem}
								storeId={store.id}
							/>
						)}
						{appointment.permissions.includes('manage discount policy') && (
							<DiscountsList
								openTab={openTab}
								products={products}
								storeId={store.id}
							/>
						)}
						{appointment.permissions.includes('manage purchase policy') && (
							<ConditionsList
								openTab={openTab}
								products={products}
								storeId={store.id}
							/>
						)}
						{appointment.permissions.includes('get history') && (
							<StorePurchaseHistory storeId={store.id} />
						)}
						<div className='offersTable'>
							<OffersTable isManager={true} store_id={storeId} />
						</div>
					</>
				)}
			</div>
			<div className={'second-tab' + (open ? ' open' : '')}>
				{Tab && (
					<div className='stick-top'>
						<Tab />
					</div>
				)}
			</div>
		</div>
	);
};

export default ManageStore;
