export type Product = {
	id: string;
	name: string;
	price: number;
	category: string;
	keywords: string[];
};
export type ProductQuantity = Product & { quantity: number };
export type StoreToSearchedProducts = { [storeID: string]: ProductToQuantity[] };
export type ProductToQuantity = [Product, number];
export type Store = { id: string; name: string; ids_to_quantities: { [key: string]: number } };
export type ShoppingCart = { bags: ShoppingBag[] };
export type ShoppingBag = {
	store_id: string;
	store_name: string;
	product_ids_to_quantities: { [productId: string]: number };
};
export type notificationTime = [string, string];
export type PurchaseDetails = {
	username: string;
	store_name: string;
	product_names: string[];
	date: Date;
	total_price: number;
};
export type Offer = {
	id: string;
	price: number;
	status:
		| 'undeclared'
		| 'awaiting manager approval'
		| 'counter offered'
		| 'approved'
		| 'rejected'
		| 'cancled';
	product_id: string;
	product_name: string;
	store_id: string;
	store_name: string;
	username: string;
	awaiting_owners: string[];
};

export type Permission =
	| 'manage products'
	| 'get appointments'
	| 'appoint manager'
	| 'remove manager'
	| 'get history'
	| 'manage purchase policy'
	| 'manage discount policy';

export const defaultPermissions: Permission[] = ['get appointments'];

export const allPermissions: Permission[] = [
	'manage products',
	'get appointments',
	'appoint manager',
	'remove manager',
	'get history',
	'manage purchase policy',
	'manage discount policy',
];

export function permissionToString(permission: Permission) {
	const map: { [key in Permission]: string } = {
		'appoint manager': 'Appoint managers',
		'get appointments': 'Get appointments',
		'get history': 'Get purchase history',
		'manage products': 'Manager products',
		'remove manager': 'Remove managers',
		'manage purchase policy': 'Manager purchase policy',
		'manage discount policy': 'Manager discount policy',
	};
	return map[permission];
}

export type Role = 'Founder' | 'Owner' | 'Manager';
export type Appointee = {
	store_id: string;
	store_name: string;
	username: string;
	role: Role;
	appointees: Appointee[];
	permissions: Permission[];
	is_manager: boolean;
};

// * Condition
// * ================================================

export type SimpleOperator = 'equals' | 'great-than' | 'less-than' | 'great-equals' | 'less-equals';

export type ConditionObjectIdentifier = 'product' | 'category';
export type ConditionObjectNoIdentifier = 'bag' | 'user';

export type ConditionObject = ConditionObjectIdentifier | ConditionObjectNoIdentifier;

export type ConditionSimple = {
	context:
		| { obj: ConditionObjectIdentifier; identifier: string }
		| { obj: ConditionObjectNoIdentifier };
	operator: SimpleOperator;
	target: number;
};

type ConditioningOperator = 'conditional';
type BasicOperator = 'and' | 'or';

export type ComplexOperator = ConditioningOperator | BasicOperator;

export type Conditioning = { operator: ConditioningOperator; test?: Condition; then?: Condition };
export type BasicRule = { operator: BasicOperator; children: Condition[] };

export type ConditionComplex = Conditioning | BasicRule;

export type Condition = { id: string } & (ConditionSimple | ConditionComplex);

export function isConditioning(rule: ConditionComplex): rule is Conditioning {
	return (rule as Conditioning).operator === 'conditional';
}
export function isBasicRule(rule: ConditionComplex): rule is BasicRule {
	return (rule as BasicRule).children !== undefined;
}

export function isConditionSimple(
	rule: ConditionSimple | ConditionComplex
): rule is ConditionSimple {
	return (rule as ConditionSimple).target !== undefined;
}
export function isConditionComplex(
	rule: ConditionSimple | ConditionComplex
): rule is ConditionComplex {
	return isConditioning(rule as ConditionComplex) || isBasicRule(rule as ConditionComplex);
}

// * Discount
// * ================================================

export type DiscountObject = 'product' | 'category' | 'store';

export type DiscountContext = { obj: 'product' | 'category'; id: string } | { obj: 'store' };

export type DiscountSimple = {
	discount_type: 'simple';
	percentage: number;
	condition?: Condition;
	context: DiscountContext;
};

export type DecisionRule = 'first' | 'max' | 'min';

export type DiscountComplexType = 'max' | 'and' | 'or' | 'xor' | 'add';

export type DiscountComplexNoneXOR = {
	type: 'max' | 'and' | 'or' | 'add';
};

export type DiscountComplexXOR = {
	type: 'xor';
	decision_rule: DecisionRule;
};

export type DiscountComplex = { discounts: Discount[]; discount_type: 'complex' } & (
	| DiscountComplexNoneXOR
	| DiscountComplexXOR
);

export type Discount = { id: string } & (DiscountSimple | DiscountComplex);

export function isDiscountSimple(
	discount: DiscountSimple | DiscountComplex
): discount is DiscountSimple {
	return (discount as DiscountSimple).percentage !== undefined;
}
export function isDiscountComplex(
	discount: DiscountSimple | DiscountComplex
): discount is DiscountComplex {
	return (discount as DiscountComplex).discounts !== undefined;
}
