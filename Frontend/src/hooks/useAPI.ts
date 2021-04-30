import axios from 'axios';
import { useState } from 'react';

export default function useAPI<Type>(endPoint: string, params?: object) {
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(false);
	const [errorMsg, setErrorMsg] = useState('');
	const [data, setData] = useState<Type | null>(null);

	const request = () =>
		axios
			.get(endPoint, {
				params: { ...params },
			})
			.then((response) => {
				if (response.status === 200) {
					setData(response.data);
				} else {
					setErrorMsg(response.statusText);
				}
			})
			.catch((error) => {
				setError(true);
				setErrorMsg(error);
			})
			.finally(() => {
				setLoading(false);
			});

	return { loading, request, error, errorMsg, data };
}
