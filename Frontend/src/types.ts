export type Product = { id: string; name: string; price: number; quantity: number };
export type Store = { id: string; name: string; role: string };
export type Appointee = { id: string; name: string; role: string; children: Appointee[] };
