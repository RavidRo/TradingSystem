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
	fatherId: string;
	onDelete?: (conditionId: string) => void;
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

const ConditionNode: FC<ConditionNodeProps> = ({ condition, onCreate, fatherId, onDelete }) => {
	const [open, setOpen] = React.useState(true);
	const handleClick = () => {
		setOpen(!open);
	};
	return (
		<>
			<ListItem button onClick={handleClick}>
				{isConditionComplex(condition.rule) && (
					<ListItemSecondaryAction onClick={handleClick}>
						<IconButton edge="start" aria-label="delete">
							{open ? <ExpandLess /> : <ExpandMore />}
						</IconButton>
					</ListItemSecondaryAction>
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
			{isConditionComplex(condition.rule) && (
				<Collapse in={open} timeout="auto">
					{isBasicRule(condition.rule) ? (
						<GenericList
							data={condition.rule.operands}
							onCreate={() => onCreate(fatherId)}
							createTxt="+ Add condition"
							padRight
						>
							{(condition) => (
								<ConditionNode
									key={condition.id}
									condition={condition}
									onCreate={onCreate}
									fatherId={condition.id}
									onDelete={onDelete}
								/>
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
										onCreate={onCreate}
										fatherId={condition.id}
										onDelete={onDelete}
									/>
								) : (
									<ListItem button onClick={() => onCreate(fatherId, 'then')}>
										<ListItemText primary="+ Add condition" />
									</ListItem>
								)}
								<ListSubheader>Only if...</ListSubheader>
								{condition.rule.test ? (
									<ConditionNode
										key={condition.id}
										condition={condition.rule.test}
										onCreate={onCreate}
										fatherId={condition.id}
										onDelete={onDelete}
									/>
								) : (
									<ListItem button onClick={() => onCreate(fatherId, 'test')}>
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
