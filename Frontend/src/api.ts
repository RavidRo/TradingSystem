import axios, { AxiosResponse } from 'axios';
import {
	Appointee,
	Condition,
	ConditionComplex,
	ConditionSimple,
	DecisionRule,
	Discount,
	DiscountComplex,
	DiscountComplexType,
	DiscountContext,
	DiscountSimple,
	Permission,
	Product,
	PurchaseDetails,
	ShoppingCart,
	Store,
	Offer,
} from './types';

function request<T>(endPoint: string, params: object, GET = true) {
	console.log(`Request ${endPoint}`, params);
	const request = GET ? axios.get : axios.post;
	return request(`/${endPoint}`, GET ? { params } : params).then((response) =>
		handleResponse<T>(response)
	);
}

function handleResponse<T>(
	response: AxiosResponse<{
		cookie: string;
		error_msg: string;
		succeeded: boolean;
		data: T;
	}>
) {
	if (response.status === 200) {
		const data = response.data;
		console.log(`The server response`, data);
		if (!data.succeeded) {
			return Promise.reject(data.error_msg);
		}
		return Promise.resolve(data.data);
	} else {
		return Promise.reject(`HTTP Error - ${response.status}`);
	}
}

function get<T>(endPoint: string, params = {}) {
	return request<T>(endPoint, params);
}
function post<T>(endPoint: string, params = {}) {
	return request<T>(endPoint, params, false);
}

export function getCookie() {
	return get<string>('get_cookie');
}

export function getProductsByStore(cookie: string, storeId: string) {
	const params = { cookie, store_id: storeId };
	return get<Product[]>('get_products_by_store', params);
}

export function register(cookie: string, username: string, password: string) {
	const params = {
		cookie,
		username,
		password,
	};
	return post<void>('register', params);
}

export function login(cookie: string, username: string, password: string) {
	const params = {
		cookie,
		username,
		password,
	};
	return post<void>('login', params);
}

export function getStoreDetails(cookie: string, storeId: string) {
	const params = { cookie, store_id: storeId };
	return get<Store>('get_stores_details', params);
}

export function searchProducts(
	cookie: string,
	productName: string,
	category: string,
	minPrice: number,
	maxPrice: number,
	keywords: string[]
) {
	const params = {
		cookie,
		product_name: productName,
		category,
		min_price: minPrice,
		max_price: maxPrice,
		kwargs: keywords,
	};
	return get<Product[]>('search_products', params);
}
export function saveProductInCart(
	cookie: string,
	storeId: string,
	productId: string,
	quantity: number
) {
	const params = { cookie, store_id: storeId, product_id: productId, quantity };
	return post<void>('save_product_in_cart', params);
}
export function getCartDetails(cookie: string) {
	const params = { cookie };
	return get<ShoppingCart>('get_cart_details', params);
}
export function removeProductFromCart(cookie: string, productId: string) {
	const params = { cookie, product_id: productId };
	return post<void>('remove_product_from_cart', params);
}
export function changeProductQuantityInCart(
	cookie: string,
	storeId: string,
	productId: string,
	quantity: number
) {
	const params = { cookie, store_id: storeId, product_id: productId, quantity };
	return post<void>('change_product_quantity_in_cart', params);
}
export function purchaseCart(cookie: string, age: number) {
	const params = { cookie, age };
	return post<number>('purchase_cart', params);
}
export function sendPayment(cookie: string, paymentDetails: object, address: object) {
	const params = { cookie, payment_details: paymentDetails, address };
	return post<void>('send_payment', params);
}
export function cancelPurchase(cookie: string) {
	const params = { cookie };
	return post<void>('cancel_purchase', params);
}
export function createStore(cookie: string, storeName: string) {
	const params = { cookie, name: storeName };
	return post<string>('create_store', params);
}
export function getPurchaseHistory(cookie: string) {
	const params = { cookie };
	return get<PurchaseDetails[]>('get_purchase_history', params);
}
export function createProduct(
	cookie: string,
	storeId: string,
	name: string,
	price: number,
	quantity: number,
	category: string,
	keywords: string[]
) {
	const params = { cookie, store_id: storeId, name, price, quantity, category, keywords };
	return post<string>('create_product', params);
}
export function removeProductFromStore(cookie: string, storeId: string, productId: string) {
	const params = { cookie, store_id: storeId, product_id: productId };
	return post<void>('remove_product_from_store', params);
}
export function changeProductQuantity(
	cookie: string,
	storeId: string,
	productId: string,
	quantity: number
) {
	const params = { cookie, store_id: storeId, product_id: productId, quantity };
	return post<void>('change_product_quantity', params);
}
export function editProductDetails(
	cookie: string,
	storeId: string,
	productId: string,
	newName: string,
	newCategory: string,
	newPrice: number,
	keywords: string[]
) {
	const params = {
		cookie,
		store_id: storeId,
		product_id: productId,
		new_name: newName,
		new_category: newCategory,
		new_price: newPrice,
		keywords,
	};
	return post<void>('edit_product_details', params);
}

export function addDiscount(
	cookie: string,
	storeId: string,
	discount: DiscountSimple | DiscountComplex,
	fatherId: string
) {
	const params = { cookie, store_id: storeId, discount_data: discount, exist_id: fatherId };
	return post<string>('add_discount', params);
}

export function moveDiscount(
	cookie: string,
	storeId: string,
	sourceNodeId: string,
	destinationNodeId: string
) {
	const params = { cookie, store_id: storeId, src_id: sourceNodeId, dest_id: destinationNodeId };
	return post<void>('move_discount', params);
}

export function getDiscounts(cookie: string, storeId: string) {
	const params = { cookie, store_id: storeId };
	return get<Discount>('get_discounts', params);
}

export function removeDiscount(cookie: string, storeId: string, discountId: string) {
	const params = { cookie, store_id: storeId, discount_id: discountId };
	return post<void>('remove_discount', params);
}

export function editSimpleDiscount(
	cookie: string,
	storeId: string,
	discountId: string,
	percentage: number,
	context: DiscountContext,
	condition?: Condition,
	duration?: number
) {
	const params = {
		cookie,
		store_id: storeId,
		discount_id: discountId,
		percentage,
		condition,
		context,
		duration,
	};
	return post<void>('edit_simple_discount', params);
}

export function editComplexDiscount(
	cookie: string,
	storeId: string,
	discountId: string,
	complexType: DiscountComplexType,
	decisionRule?: DecisionRule
) {
	const params = {
		cookie,
		store_id: storeId,
		discount_id: discountId,
		complex_type: complexType,
		decision_rule: decisionRule,
	};
	return post<void>('edit_complex_discount', params);
}

export function appointOwner(cookie: string, storeId: string, username: string) {
	const params = { cookie, store_id: storeId, username };
	return post<void>('appoint_owner', params);
}

export function appointManager(cookie: string, storeId: string, username: string) {
	const params = { cookie, store_id: storeId, username };
	return post<void>('appointManager', params);
}

export function addManagerPermission(
	cookie: string,
	storeId: string,
	username: string,
	permission: Permission
) {
	const params = { cookie, store_id: storeId, username, permission };
	return post<void>('add_manager_permission', params);
}

export function removeManagerPermission(
	cookie: string,
	storeId: string,
	username: string,
	permission: Permission
) {
	const params = { cookie, store_id: storeId, username, permission };
	return post<void>('remove_manager_permission', params);
}

export function removeAppointment(cookie: string, storeId: string, username: string) {
	const params = { cookie, store_id: storeId, username };
	return post<void>('remove_appointment', params);
}

export function getStoreAppointments(cookie: string, storeId: string) {
	const params = { cookie, store_id: storeId };
	return get<Appointee[]>('get_store_appointments', params);
}

export function getMyAppointments(cookie: string) {
	const params = { cookie };
	return get<Appointee[]>('get_my_appointments', params);
}

export function addPurchaseRule(
	cookie: string,
	storeId: string,
	ruleDetails: ConditionSimple | ConditionComplex,
	ruleType: 'simple' | 'complex',
	parentId: string,
	clause?: 'test' | 'then'
) {
	const params = {
		cookie,
		store_id: storeId,
		rule_details: ruleDetails,
		rule_type: ruleType,
		parent_id: parentId,
		clause,
	};
	return post<string>('add_purchase_rule', params);
}

export function removePurchaseRule(cookie: string, storeId: string, ruleId: string) {
	const params = { cookie, store_id: storeId, rule_id: ruleId };
	return post<void>('remove_purchase_rule', params);
}

export function editPurchaseRule(
	cookie: string,
	storeId: string,
	ruleDetails: ConditionSimple | ConditionComplex,
	ruleId: string,
	ruleType: 'simple' | 'complex'
) {
	const params = {
		cookie,
		store_id: storeId,
		rule_details: ruleDetails,
		rule_id: ruleId,
		rule_type: ruleType,
	};
	return post<void>('edit_purchase_rule', params);
}

export function movePurchaseRule(
	cookie: string,
	storeId: string,
	ruleId: string,
	newParentId: string
) {
	const params = { cookie, store_id: storeId, rule_id: ruleId, new_parent_id: newParentId };
	return post<void>('move_purchase_rule', params);
}

export function getStorePurchaseHistory(cookie: string, storeId: string) {
	const params = { cookie, store_id: storeId };
	return get<PurchaseDetails[]>('get_store_purchase_history', params);
}

export function getAnyStorePurchaseHistory(cookie: string, storeId: string) {
	const params = { cookie, store_id: storeId };
	return get<PurchaseDetails[]>('get_any_store_purchase_history', params);
}

export function getUserPurchaseHistory(cookie: string, storeId: string) {
	const params = { cookie, store_id: storeId };
	return get<PurchaseDetails[]>('get_user_purchase_history', params);
}

export function emptyNotifications(cookie: string) {
	const params = { cookie };
	return post<void>('empty_notifications', params);
}

export function getPurchasePolicy(cookie: string, storeId: string) {
	const params = { cookie, store_id: storeId };
	return get<Condition>('get_purchase_policy', params);
}
export function getUserOffers(cookie: string) {
	const params = { cookie };
	return get<Offer[]>('get_user_offers', params);
}
