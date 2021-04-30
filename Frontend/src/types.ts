export type Product = {
	id: string;
	name: string;
	price: number;
	quantity: number;
	category: string;
	keywords: string[];
};
export type Store = { id: string; name: string; role: string };
export type Permission =
	| 'manage_products'
	| 'get_appointments'
	| 'appoint_manager'
	| 'remove_manager'
	| 'get_history';

export type Role = 'Founder' | 'Owner' | 'Manager';
export type Appointee = {
	id: string;
	name: string;
	role: Role;
	children: Appointee[];
	permissions?: { [key in Permission]: boolean };
};

// * Condition
// * ================================================

export type SimpleOperator = 'equals' | 'great-than' | 'less-than' | 'great-equals' | 'less-equals';

export type ConditionSimple = {
	context: { obj: 'product' | 'category'; identifier: string } | { obj: 'bag' | 'user' };
	operator: SimpleOperator;
	target: number;
};

type Conditioning = { operator: 'conditioning'; test?: Condition; then?: Condition };
type BasicOperator = { operator: 'and' | 'or'; operands: Condition[] };

type ConditionComplex = Conditioning | BasicOperator;

export type Condition = { id: string; rule: ConditionSimple | ConditionComplex };

export function isConditioning(rule: ConditionComplex): rule is Conditioning {
	return (rule as Conditioning).operator === 'conditioning';
}
export function isBasicOperator(rule: ConditionComplex): rule is BasicOperator {
	return (rule as BasicOperator).operands !== undefined;
}

export function isConditionSimple(
	rule: ConditionSimple | ConditionComplex
): rule is ConditionSimple {
	return (rule as ConditionSimple).target !== undefined;
}
export function isConditionComplex(
	rule: ConditionSimple | ConditionComplex
): rule is ConditionComplex {
	return isConditioning(rule as ConditionComplex) || isBasicOperator(rule as ConditionComplex);
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
