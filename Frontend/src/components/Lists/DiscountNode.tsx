import React, { FC, useState } from 'react';
import {
	Collapse,
	IconButton,
	ListItem,
	ListItemSecondaryAction,
	ListItemText,
} from '@material-ui/core';
import { ExpandLess, ExpandMore } from '@material-ui/icons';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';
import EditIcon from '@material-ui/icons/Edit';

import { DecisionRule, Discount, isDiscountComplex, isDiscountSimple } from '../../types';
import GenericList from './GenericList';
import SecondaryActionButton from './SecondaryActionButton';

type DiscountNodeProps = {
	discount: Discount;
	onCreate: (father_id: string) => void;
	onDelete: (discountId: string) => void;
	onEdit: (discount: Discount) => void;
	productIdToString: (productId: string) => string;
	onMove: (srcId: string, destId: string) => void;
};

const DiscountNode: FC<DiscountNodeProps> = ({
	discount,
	onCreate,
	onDelete,
	productIdToString,
	onEdit,
	onMove,
}) => {
	const [open, setOpen] = useState(false);
	const handleClick = () => {
		setOpen(!open);
	};

	function decisionRuleToString(decisionRule: DecisionRule): string {
		const ruleToString: { [key in DecisionRule]: string } = {
			first: 'first discount',
			max: 'best discount value',
			min: 'worst discount value',
		};
		return ruleToString[decisionRule];
	}

	function discountToString(discount: Discount) {
		if (isDiscountSimple(discount)) {
			const discountOn =
				discount.context.obj === 'store'
					? 'all products'
					: discount.context.obj === 'category'
					? `all products in the ${discount.context.id} category`
					: `product "${productIdToString(discount.context.id)}"`;
			return `${discount.percentage}% discount on ${discountOn}`;
		} else {
			return `${discount.type.toUpperCase()}${
				discount.type === 'xor'
					? ` - decision rule: ${decisionRuleToString(discount.decision_rule)}`
					: ''
			}`;
		}
	}

	const onDragStart = (event: React.DragEvent) => {
		event.dataTransfer.setData('text', discount.id);
		// Disabling the drag ghost image
		const img = new Image();
		img.src = 'data:image/gif;base64,R0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=';
		event.dataTransfer.setDragImage(img, 0, 0);
	};
	const onDragOver = (event: React.DragEvent) => {
		if (isDiscountComplex(discount)) {
			event.preventDefault();
		}
	};
	const onDrop = (event: React.DragEvent<HTMLDivElement>) => {
		if (isDiscountComplex(discount)) {
			event.preventDefault();
			const draggableElementData = event.dataTransfer.getData('text');
			onMove(draggableElementData, discount.id);
		}
	};

	return (
		<>
			<div draggable="true" onDragStart={onDragStart} onDragOver={onDragOver} onDrop={onDrop}>
				<ListItem button onClick={handleClick} className="discount-node">
					{isDiscountComplex(discount) && (
						<IconButton edge="start" aria-label="delete">
							{open ? <ExpandLess /> : <ExpandMore />}
						</IconButton>
					)}
					<ListItemText primary={discountToString(discount)} />
					{onDelete && (
						<ListItemSecondaryAction>
							<SecondaryActionButton onClick={() => onEdit(discount)}>
								<EditIcon />
							</SecondaryActionButton>
							<SecondaryActionButton onClick={() => onDelete(discount.id)}>
								<DeleteForeverOutlinedIcon />
							</SecondaryActionButton>
						</ListItemSecondaryAction>
					)}
				</ListItem>
			</div>
			{isDiscountComplex(discount) && (
				<Collapse in={open} timeout="auto">
					<GenericList
						data={discount.discounts}
						onCreate={() => onCreate(discount.id)}
						createTxt="+ Add new discount"
						padRight
					>
						{(discount) => (
							<DiscountNode
								key={discount.id}
								discount={discount}
								onCreate={onCreate}
								onDelete={onDelete}
								productIdToString={productIdToString}
								onEdit={onEdit}
								onMove={onMove}
							/>
						)}
					</GenericList>
				</Collapse>
			)}
		</>
	);
};

export default DiscountNode;
