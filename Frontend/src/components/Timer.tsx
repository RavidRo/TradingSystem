import React, { FC, useState } from 'react';
import useInterval from '../hooks/useInterval';
import '../styles/Timer.scss';

type TimerProps = {};

const Timer: FC<TimerProps> = () => {
	const [timeLeft, setTimeLeft] = useState<number>(600);

	useInterval(() => {
		if (timeLeft > 0) {
			setTimeLeft(timeLeft - 1);
		}
	}, 1000);

	const stringOfTime = () => {
		if (timeLeft === 0) {
			return 'Time Over!';
		}
		if (timeLeft < 60) {
			return '00:' + timeLeft;
		} else {
			return '' + Math.floor(timeLeft / 60) + ':' + Math.floor(timeLeft % 60);
		}
	};
	return (
		<div className='timerDiv'>
			<h3>
				Time left for entering details:
				<div
					className='timer'
					style={{ border: '#ff0000', borderWidth: '3px', borderStyle: 'solid' }}
				>
					<h3>{stringOfTime()}</h3>
				</div>
			</h3>
		</div>
	);
};

export default Timer;
