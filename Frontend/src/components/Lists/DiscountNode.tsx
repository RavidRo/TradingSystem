import React, { FC, useState } from 'react';
import {
	Collapse,
	IconButton,
	ListItem,
	ListItemSecondaryAction,
	ListItemText,
} from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';

import { DecisionRule, Discount, isDiscountComplex, isDiscountSimple } from '../../types';
import GenericList from './GenericList';

type DiscountNodeProps = {
	discount: Discount;
	onCreate: (father_id: string) => void;
	fatherId: string;
};

function discountToString(discount: Discount) {
	const rule = discount.rule;
	if (isDiscountSimple(rule)) {
		const discountOn =
			rule.context.obj === 'store'
				? 'all products'
				: rule.context.obj === 'category'
				? `all products in the ${rule.context.identifier} category`
				: `product "${rule.context.identifier}"`;
		return `${rule.percentage}% discount on ${discountOn}`;
	} else {
		const type = rule.type;
		return `${type.operator.toUpperCase()}${
			type.operator === 'xor'
				? ` - decision rule: ${decisionRuleToString(type.decision_rule)}`
				: ''
		}`;
	}
}

function decisionRuleToString(decisionRule: DecisionRule): string {
	const ruleToString: { [key in DecisionRule]: string } = {
		first: 'first discount',
		max: 'best discount value',
		min: 'worst discount value',
	};
	return ruleToString[decisionRule];
}

const DiscountNode: FC<DiscountNodeProps> = ({ discount, onCreate, fatherId }) => {
	const [open, setOpen] = useState(false);
	const handleClick = () => {
		setOpen(!open);
	};
	return (
		<>
			<ListItem
				button
				// selected={isSelected(appointee)}
				// onClick={() => onClick(appointee)}
			>
				<ListItemText primary={discountToString(discount)} />
				{isDiscountComplex(discount.rule) && (
					<ListItemSecondaryAction onClick={handleClick}>
						<IconButton edge="start" aria-label="delete">
							{open ? <ExpandLess /> : <ExpandMore />}
						</IconButton>
					</ListItemSecondaryAction>
				)}
			</ListItem>
			{isDiscountComplex(discount.rule) && (
				<Collapse in={open} timeout="auto">
					<GenericList
						data={discount.rule.operands}
						onCreate={() => onCreate(fatherId)}
						createTxt="+ Add new discount"
						padRight
					>
						{(discount) => (
							<DiscountNode
								key={discount.id}
								discount={discount}
								onCreate={onCreate}
								fatherId={discount.id}
							/>
						)}
					</GenericList>
				</Collapse>
			)}
		</>
	);
};

export default DiscountNode;
