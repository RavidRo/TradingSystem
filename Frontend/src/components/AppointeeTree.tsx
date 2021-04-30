import React, { FC } from 'react';
import { Appointee } from '../types';
import GenericList from './GenericList';
import AppointeeNode from './AppointeeNode';
// import '../styles/AppointeeTree.scss';

const tree: Appointee[] = [
	{
		id: '1',
		name: 'Sean',
		role: 'Lover',
		children: [
			{
				id: '1',
				name: 'Sean',
				role: 'Lover',
				children: [
					{
						id: '0',
						name: 'Tali',
						role: 'Owner',
						children: [],
					},
				],
			},
			{
				id: '2',
				name: 'Sean',
				role: 'Lover',
				children: [],
			},
		],
	},
];

type AppointeeTreeProps = {};

const AppointeeTree: FC<AppointeeTreeProps> = () => {
	return (
		<GenericList data={['']} header="Store's appointments">
			{(_) => (
				<>
					<AppointeeNode appointees={tree} />
				</>
			)}
		</GenericList>
	);
};

export default AppointeeTree;
