import axios from 'axios';
import { useContext, useState } from 'react';
import { CookieContext } from '../contexts';
import Swal from 'sweetalert2';

export function useAPI2<T extends unknown[], R = unknown>(
	apiFunc: (cookie: string, ...args: T) => Promise<R>
) {
	const [loading, setLoading] = useState<boolean>(false);
	const [error, setError] = useState<boolean>(false);
	const [errorMsg, setErrorMsg] = useState<string>('');
	const [data, setData] = useState<R | null>(null);
	const cookie = useContext(CookieContext);

	const request = (...params: T): Promise<R> => {
		setLoading(true);
		setError(false);
		setErrorMsg('');
		setData(null);

		return apiFunc(cookie, ...params)
			.then((data) => {
				setData(data);
				return data;
			})
			.catch((errorMsg) => {
				setError(true);
				setErrorMsg(errorMsg);
				Swal.fire({
					icon: 'error',
					title: 'Oops...',
					text: errorMsg,
				});
				return Promise.reject(errorMsg);
			})
			.finally(() => {
				setLoading(false);
			});
	};

	return { request, loading, error, errorMsg, data };
}

export default function useAPI<Type>(
	endPoint: string,
	dynamicParams?: object,
	type: 'GET' | 'POST' = 'GET'
) {
	type APIResponse = {
		cookie: string;
		error_msg: string;
		succeeded: boolean;
		data: Type;
	};

	const [loading, setLoading] = useState<boolean>(true);
	const [error, setError] = useState<boolean>(false);
	const [errorMsg, setErrorMsg] = useState<string>('');
	const [data, setData] = useState<APIResponse | null>(null);
	const cookie = useContext(CookieContext);
	const defaultParams = { cookie };

	const request = (
		moreParams?: object,
		callback?: (data: APIResponse | null, error: boolean, errorMsg: string) => void
	) => {
		setLoading(true);
		setError(false);
		setErrorMsg('');
		setData(null);

		const params = { ...defaultParams, ...dynamicParams, ...moreParams };
		console.log('Params sent: ', params);

		const promise =
			type === 'GET'
				? axios.get(endPoint, {
						params,
				  })
				: axios.post(endPoint, params);

		let dataVar: APIResponse | null = null;
		let errorVar: boolean = false;
		let errorMsgVar: string = '';

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
				errorVar = errorVar || (dataVar !== null && !dataVar.succeeded);
				setError(errorVar);
				setLoading(false);
				setData(dataVar);
				errorMsgVar = dataVar?.error_msg ? dataVar?.error_msg : errorMsgVar;
				setErrorMsg(errorMsgVar);
				console.log({ endPoint, data: dataVar, error: errorVar, errorMsg: errorMsgVar });
				if (errorVar) {
					Swal.fire({
						icon: 'error',
						title: 'Oops...',
						text: errorMsgVar,
					});
				}
			})
			.then(() => {
				callback && callback(dataVar, errorVar, errorMsgVar);
				return { data: dataVar, error: errorVar, errorMsg: errorMsgVar };
			});
	};

	return { loading, request, error, errorMsg, data };
}
