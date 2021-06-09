import Swal from 'sweetalert2';

export function areYouSure<T extends unknown[], R = unknown>(
	func: (...args: T) => R,
	text: string = '',
	confirmText: string = 'Confirm!'
) {
	return (...params: T): void => {
		Swal.fire({
			title: 'Are you sure?',
			text: text,
			icon: 'warning',
			showCancelButton: true,
			confirmButtonColor: '#3085d6',
			cancelButtonColor: '#d33',
			confirmButtonText: confirmText,
		}).then((result) => {
			if (result.isConfirmed) {
				func(...params);
			}
		});
	};
}

export function confirm(headerText: string = '', text: string = '') {
	Swal.fire(headerText, text, 'success');
}

export function confirmOnSuccess<T extends unknown[]>(
	func: (...args: T) => Promise<unknown>,
	headerText: string = '',
	text: string = ''
) {
	return (...params: T): Promise<unknown> => {
		return func(...params).then(() => {
			confirm(headerText, text);
		});
	};
}
