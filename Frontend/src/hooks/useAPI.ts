import axios from 'axios';
import { useContext, useState } from 'react';
import { CookieContext } from '../contexts';

export default function useAPI<Type>(
	endPoint: string,
	params?: object,
	type: 'GET' | 'POST' = 'GET'
) {
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState(false);
	const [errorMsg, setErrorMsg] = useState('');
	const [data, setData] = useState<Type | null>(null);
	const cookie = useContext(CookieContext);

	const defaultParams = { cookie };

	const request = (moreParams?: object) => {
		const promise =
			type === 'GET'
				? axios.get(endPoint, {
						params: { ...defaultParams, ...params, ...moreParams },
				  })
				: axios.post(endPoint, {
						...defaultParams,
						...params,
						...moreParams,
				  });

		return promise
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
	};

	return { loading, request, error, errorMsg, data };
}
