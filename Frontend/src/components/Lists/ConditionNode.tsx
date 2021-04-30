import React, { FC } from 'react';

import {
	Collapse,
	IconButton,
	List,
	ListItem,
	ListItemSecondaryAction,
	ListItemText,
	ListSubheader,
} from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';

import {
	Condition,
	ConditionSimple,
	isBasicOperator,
	isConditionComplex,
	isConditionSimple,
	SimpleOperator,
} from '../../types';
import GenericList from './GenericList';
// import '../styles/ConditionNode.scss';

type ConditionNodeProps = {
	condition: Condition;
};

function conditionToString(condition: Condition): string {
	const rule = condition.rule;
	if (isConditionSimple(rule)) {
		return `${conditionSimpleContextToString(rule)} ${operatorToString(rule.operator)} ${
			rule.target
		}`;
	} else {
		return rule.operator.toUpperCase();
	}
}

function conditionSimpleContextToString(rule: ConditionSimple): string {
	return rule.context.obj === 'bag'
		? 'Number of products in bag'
		: rule.context.obj === 'user'
		? 'The user age'
		: rule.context.obj === 'category'
		? `The number of product in the category "${rule.context.identifier}"`
		: rule.context.obj === 'product'
		? `The number of product of type ${rule.context.identifier}`
		: '';
}
function operatorToString(operator: SimpleOperator): string {
	const mapToString: { [key in SimpleOperator]: string } = {
		'great-equals': '>=',
		'great-than': ' >',
		'less-equals': '<=',
		'less-than': '<',
		equals: '=',
	};
	return mapToString[operator];
}

const ConditionNode: FC<ConditionNodeProps> = ({ condition }) => {
	const [open, setOpen] = React.useState(true);
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
				<ListItemText primary={conditionToString(condition)} />
				{isConditionComplex(condition.rule) && (
					<ListItemSecondaryAction onClick={handleClick}>
						<IconButton edge="start" aria-label="delete">
							{open ? <ExpandLess /> : <ExpandMore />}
						</IconButton>
					</ListItemSecondaryAction>
				)}
			</ListItem>
			{isConditionComplex(condition.rule) && (
				<Collapse in={open} timeout="auto">
					{isBasicOperator(condition.rule) ? (
						<GenericList
							data={condition.rule.operands}
							onCreate={() => {}}
							createTxt="+ Add condition"
							padRight
						>
							{(condition) => (
								<ConditionNode key={condition.id} condition={condition} />
							)}
						</GenericList>
					) : (
						<div className="list-padding">
							<List>
								<ListSubheader>You can buy...</ListSubheader>
								{condition.rule.then ? (
									<ConditionNode
										key={condition.id}
										condition={condition.rule.then}
									/>
								) : (
									<ListItem
										button
										// onClick={onCreate}
									>
										<ListItemText primary="+ Add condition" />
									</ListItem>
								)}
								<ListSubheader>Only if...</ListSubheader>
								{condition.rule.test ? (
									<ConditionNode
										key={condition.id}
										condition={condition.rule.test}
									/>
								) : (
									<ListItem
										button
										// onClick={onCreate}
									>
										<ListItemText primary="+ Add condition" />
									</ListItem>
								)}
							</List>
						</div>
					)}
				</Collapse>
			)}
		</>
	);
};

export default ConditionNode;
