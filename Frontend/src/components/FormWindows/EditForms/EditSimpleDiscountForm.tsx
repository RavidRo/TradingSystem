import React, { FC, useState } from 'react';
import { DiscountObject, DiscountSimple, Product } from '../../../types';
import FormWindow from '../FormWindow';
import SimpleDiscountForm from '../SimpleDiscountForm';

type EditSimpleDiscountFormProps = {
	onSubmit: (discount: DiscountSimple) => void;
	products: Product[];
	discountToEdit: DiscountSimple;
};

const EditSimpleDiscountForm: FC<EditSimpleDiscountFormProps> = ({
	onSubmit,
	products,
	discountToEdit,
}) => {
	const [percentage, setPercentage] = useState<string>(`${discountToEdit.percentage}`);
	const [contextObject, setContextObject] = useState<DiscountObject | ''>(
		discountToEdit.context.obj
	);
	const [contextIdentifier, setContextIdentifier] = useState<string>(
		discountToEdit.context.obj === 'store' ? '' : discountToEdit.context.id
	);

	const [percentageError, setPercentageError] = useState<boolean>(false);

	function handleSubmit() {
		setPercentageError(+percentage < 0);
		if (!percentageError) {
			if (contextObject !== '') {
				if (contextObject === 'store') {
					onSubmit({
						percentage: +percentage,
						context: {
							obj: contextObject,
						},
						discount_type: 'simple',
					});
				} else if (contextIdentifier !== '') {
					onSubmit({
						percentage: +percentage,
						context: {
							obj: contextObject,
							id: contextIdentifier,
						},
						discount_type: 'simple',
					});
				}
			}
		}
	}

	return (
		<FormWindow handleSubmit={handleSubmit} submitText="Confirm!" header="Edit discount">
			<SimpleDiscountForm
				contextIdentifier={contextIdentifier}
				contextObject={contextObject}
				percentageError={percentageError}
				setContextIdentifier={setContextIdentifier}
				setContextObject={setContextObject}
				products={products}
				setPercentage={setPercentage}
				defaultDiscount={discountToEdit}
			/>
		</FormWindow>
	);
};

export default EditSimpleDiscountForm;
