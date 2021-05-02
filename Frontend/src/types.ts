export type Product = {
	id: string;
	name: string;
	price: number;
	category: string;
	keywords: string[];
};
export type ProductQuantity = Product & { quantity: number };
export type StoreToSearchedProducts = {storeID:string, productQuantities:ProductToQuantity[]}[];
export type ProductToQuantity = [Product,number];
export type Store = { id: string; name: string; ids_to_quantities: { [key: string]: number } };
export type ShoppingCart = {bags:ShoppingBag[]};
export type ShoppingBag = {storeID:string, storeName:string,prodQuantities:ProductToQuantity[]};


export type Permission =
	| 'manage_products'
	| 'get_appointments'
	| 'appoint_manager'
	| 'remove_manager'
	| 'get_history';

export const defaultPermissions = {
	manage_products: false,
	get_appointments: true,
	appoint_manager: false,
	remove_manager: false,
	get_history: false,
};

export type Role = 'Founder' | 'Owner' | 'Manager';
export type Appointee = {
	store_id: string;
	store_name: string;
	username: string;
	role: Role;
	appointees: Appointee[];
	permissions: { [key in Permission]: boolean };
	isManager: boolean;
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

type ConditioningOperator = 'conditioning';
type BasicOperator = 'and' | 'or';

export type ComplexOperator = ConditioningOperator | BasicOperator;

export type Conditioning = { operator: ConditioningOperator; test?: Condition; then?: Condition };
export type BasicRule = { operator: BasicOperator; operands: Condition[] };

export type ConditionComplex = Conditioning | BasicRule;

export type Condition = { id: string; rule: ConditionSimple | ConditionComplex };

export function isConditioning(rule: ConditionComplex): rule is Conditioning {
	return (rule as Conditioning).operator === 'conditioning';
}
export function isBasicRule(rule: ConditionComplex): rule is BasicRule {
	return (rule as BasicRule).operands !== undefined;
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

export type DiscountSimple = {
	percentage: number;
	condition?: Condition;
	context: { obj: 'product' | 'category'; identifier: string } | { obj: 'store' };
};

export type DecisionRule = 'first' | 'max' | 'min';

export type Operator = 'max' | 'and' | 'or' | 'xor';

type DiscountComplexNoneXOR = { operator: 'max' | 'and' | 'or' };
type DiscountComplexXOR = { operator: 'xor'; decision_rule: DecisionRule };

export type DiscountComplex = {
	type: DiscountComplexNoneXOR | DiscountComplexXOR;
	operands: Discount[];
};

export type Discount = { id: string; rule: DiscountSimple | DiscountComplex };

export function isDiscountSimple(rule: DiscountSimple | DiscountComplex): rule is DiscountSimple {
	return (rule as DiscountSimple).percentage !== undefined;
}
export function isDiscountComplex(rule: DiscountSimple | DiscountComplex): rule is DiscountComplex {
	return (rule as DiscountComplex).operands !== undefined;
}
