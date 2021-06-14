import { GridList, GridListTile } from '@material-ui/core';
import React, { FC, useEffect } from 'react';
import Box from '@material-ui/core/Box';
import { faEnvelopeOpenText } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import '../styles/Notifications.scss';
import { notificationTime } from '../types';

type NotificationProps = {
	location: any;
	initializeNotifications: () => void;
};

const Notifications: FC<NotificationProps> = ({ location, initializeNotifications }) => {
	const notifications: notificationTime[] = location.state.notifications;
	useEffect(() => {
		initializeNotifications();
	}, []);

	return (
		<div className='NotificationsDiv'>
			<GridList cellHeight={130} cols={1}>
				{notifications.map((_, index) => (
					<Box className='box' color='black' bgcolor='#fbd1b7' m={1}>
						<FontAwesomeIcon className='messageIcon' icon={faEnvelopeOpenText} />
						<GridListTile key={index}>
							<h3 className='notify'>{notifications[index][0]}</h3>
							<h3 className='date'>{notifications[index][1]}</h3>
						</GridListTile>
					</Box>
				))}
			</GridList>
		</div>
	);
};

export default Notifications;
