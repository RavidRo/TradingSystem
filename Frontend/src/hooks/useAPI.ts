import axios from 'axios';
import { useContext, useState } from 'react';
import { CookieContext } from '../contexts';

export default function useAPI<Type>(
	endPoint: string,
	dynamicParams?: object,
	type: 'GET' | 'POST' = 'GET'
) {
	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<boolean>(false);
	const [errorMsg, setErrorMsg] = useState<string>('');
	const [data, setData] = useState<Type | null>(null);
	const cookie = useContext(CookieContext);

	const defaultParams = { cookie };

	const request = (
		moreParams?: object,
		callback?: (data: Type | null, error: boolean, errorMsg: string) => void
	) => {
		setLoading(true);
		setError(false);
		setErrorMsg('');
		setData(null);

		const params = { ...defaultParams, ...dynamicParams, ...moreParams };
		console.log(params);

		const promise =
			type === 'GET'
				? axios.get(endPoint, {
						params,
				  })
				: axios.post(endPoint, params);

		let dataVar = data;
		let errorVar = error;
		let errorMsgVar = errorMsg;

		return promise
			.then((response) => {
				if (response.status === 200) {
					dataVar = response.data;
				} else {
					errorVar = true;
					errorMsgVar = response.statusText;
				}
			})
			.catch((error) => {
				errorVar = true;
				errorMsgVar = error;
			})
			.finally(() => {
				setError(errorVar);
				setLoading(false);
				setData(dataVar);
				setErrorMsg(errorMsgVar);
				console.log({ data: dataVar, error: errorMsgVar });
			})
			.then(() => {
				callback && callback(dataVar, errorVar, errorMsgVar);
				return { data: dataVar, error: errorVar, errorMsg: errorMsgVar };
			});
	};

	return { loading, request, error, errorMsg, data };
}
