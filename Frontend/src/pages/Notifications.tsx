import { GridList, GridListTile } from '@material-ui/core';
import React, { FC,useState,useEffect} from 'react';
import Box from '@material-ui/core/Box';
import {faEnvelopeOpenText} from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import '../styles/Notifications.scss';

type NotificationProps = {
    location: any,
};

const Notifications: FC<NotificationProps> = ({location}) => {
    const [notifications, setNotifications] = useState<string[]>(location.state.notifications);

    useEffect(()=>{
        setNotifications(location.state.notifications);
    },[location.state.notifications]);

	return (
        <div className="NotificationsDiv">
            <GridList cellHeight={130} cols={1}>
                {notifications.map((notification) => (
                    <Box className="box" color="black" bgcolor="pink" m={1}>
                        <FontAwesomeIcon className="messageIcon" icon={faEnvelopeOpenText} />
                        <GridListTile key={notifications.indexOf(notification)}>
                            <h3 className="notify">{notification}</h3>
                        </GridListTile>
                    </Box>
                ))}
            </GridList>
        </div>
	);
};

export default Notifications;
