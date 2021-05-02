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
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';

import {
	Condition,
	ConditionSimple,
	isBasicRule,
	isConditionComplex,
	isConditionSimple,
	SimpleOperator,
} from '../../types';
import GenericList from './GenericList';
// import '../styles/ConditionNode.scss';

type ConditionNodeProps = {
	condition: Condition;
	onCreate: (fatherId: string, conditioning?: 'test' | 'then' | undefined) => void;
	onDelete?: (conditionId: string) => void;
	productIdToName: (productId: string) => string;
};

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

const ConditionNode: FC<ConditionNodeProps> = ({
	condition,
	onCreate,
	onDelete,
	productIdToName,
}) => {
	const [open, setOpen] = React.useState(true);
	const handleClick = () => {
		setOpen(!open);
	};

	const conditionSimpleContextToString = (rule: ConditionSimple): string => {
		return rule.context.obj === 'bag'
			? 'Number of products in bag'
			: rule.context.obj === 'user'
			? 'The user age'
			: rule.context.obj === 'category'
			? `The number of product in the category "${rule.context.identifier}"`
			: rule.context.obj === 'product'
			? `The number of product of type ${productIdToName(rule.context.identifier)}`
			: '';
	};

	const conditionToString = (condition: Condition): string => {
		if (isConditionSimple(condition)) {
			return `${conditionSimpleContextToString(condition)} ${operatorToString(
				condition.operator
			)} ${condition.target}`;
		} else {
			return condition.operator.toUpperCase();
		}
	};

	return (
		<>
			<ListItem button onClick={handleClick}>
				{isConditionComplex(condition) && (
					<IconButton edge="start" aria-label="delete">
						{open ? <ExpandLess /> : <ExpandMore />}
					</IconButton>
				)}
				<ListItemText primary={conditionToString(condition)} />
				{onDelete && (
					<ListItemSecondaryAction onClick={() => onDelete(condition.id)}>
						<IconButton edge="end" aria-label="delete">
							<DeleteForeverOutlinedIcon />
						</IconButton>
					</ListItemSecondaryAction>
				)}
			</ListItem>
			{isConditionComplex(condition) && (
				<Collapse in={open} timeout="auto">
					{isBasicRule(condition) ? (
						<GenericList
							data={condition.children}
							onCreate={() => onCreate(condition.id)}
							createTxt="+ Add condition"
							padRight
						>
							{(currentCondition) => (
								<ConditionNode
									key={currentCondition.id}
									condition={currentCondition}
									onCreate={onCreate}
									onDelete={onDelete}
									productIdToName={productIdToName}
								/>
							)}
						</GenericList>
					) : (
						<div className="list-padding">
							<List>
								<ListSubheader>You can buy...</ListSubheader>
								{condition.then ? (
									<ConditionNode
										key={condition.then.id}
										condition={condition.then}
										onCreate={onCreate}
										onDelete={onDelete}
										productIdToName={productIdToName}
									/>
								) : (
									<ListItem button onClick={() => onCreate(condition.id, 'then')}>
										<ListItemText primary="+ Add condition" />
									</ListItem>
								)}
								<ListSubheader>Only if...</ListSubheader>
								{condition.test ? (
									<ConditionNode
										key={condition.test.id}
										condition={condition.test}
										onCreate={onCreate}
										onDelete={onDelete}
										productIdToName={productIdToName}
									/>
								) : (
									<ListItem button onClick={() => onCreate(condition.id, 'test')}>
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
