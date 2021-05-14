import React, { FC,useState,useEffect} from 'react';


type NotificationProps = {
    location: any,
};

const Notifications: FC<NotificationProps> = ({location}) => {
    console.log(location.state);
    const [notifications, setNotifications] = useState<string[]>(location.state.notifications);

    useEffect(()=>{
        setNotifications(location.state.notifications);
    },[location.state.notifications]);

	return (
        <div className="NotificationsDiv">
            <ul>
                {notifications.map((notification)=>{
                    return (<li>{notification}</li>)
                })}
            </ul>
        </div>
	);
};

export default Notifications;
