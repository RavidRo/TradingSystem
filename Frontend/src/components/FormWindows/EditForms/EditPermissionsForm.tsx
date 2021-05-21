import React, { FC, useState } from 'react';

import { Appointee, Permission } from '../../../types';
import FormWindow from '../FormWindow';
import PermissionsList from '../../PermissionsList';

type EditPermissionsFormProps = {
	appointee: Appointee;
	onSubmit: (permissions: Permission[]) => void;
};

const EditPermissionsForm: FC<EditPermissionsFormProps> = ({ appointee, onSubmit }) => {
	const [permissions, setPermissions] = useState<Permission[]>(appointee.permissions);

	return (
		<FormWindow
			handleSubmit={() => onSubmit(permissions)}
			header="Edit permissions"
			submitText="Confirm"
		>
			<PermissionsList permissions={permissions} setPermissions={setPermissions} />
		</FormWindow>
	);
};

export default EditPermissionsForm;
