
import { Button} from '@material-ui/core';
import React ,{FC, useEffect, useState} from 'react';
import CartProduct from '../components/CartProduct';
import PurchaseIcon from '@material-ui/icons/LocalMall';
import { Link } from 'react-router-dom';
import '../styles/Bag.scss';
import {Product,ProductQuantity,Store} from '../types';
import useAPI from '../hooks/useAPI';

type BagProps = {
	storeID:string,
    products:ProductQuantity[],
    propHandleDelete:(productID:string)=>void,
    propHandleAdd:(product:Product,storeID:string)=>Promise<boolean>;
    changeQuantity:(store:string,product:string,quan:number)=>void,
};

const Bag: FC<BagProps> = ({storeID,products,propHandleDelete,changeQuantity,propHandleAdd}:BagProps) => {

    const [productsInCart,setProducts] = useState<ProductQuantity[]>(products);
    const [storeName,setStoreName] =  useState<string>("");

	const storeIDToNameObj = useAPI<Store>('/get_store',{store_id:storeID});
    useEffect(()=>{
        storeIDToNameObj.request().then(({ data, error, errorMsg }) => {
            if (!error && data !== null) {
                setStoreName(data.data.name);
            }
            else{
                alert(errorMsg);
            }
    })},[]);

    useEffect(()=>{
        setProducts(products);
		setTotal(calculateTotal());
    },[products]);

	const calculateTotal = ()=>{
		const reducer = (accumulator:number, currentValue:ProductQuantity) => accumulator + (currentValue.price*currentValue.quantity);
		return productsInCart.reduce(reducer,0);
	}
	const [total,setTotal] = useState<number>(calculateTotal());

	//when clicking the X besides the product in cart
	const onRemove = (id: string) => {
		setProducts(productsInCart.filter((product) => product.id !== id));
		propHandleDelete(id);//updating server
	}
   
	const getQuanOfProduct = (id:string)=>{
		for(var i=0;i<productsInCart.length;i++){
			if(productsInCart[i].id===id){
				return productsInCart[i].quantity;
			}
		}
		return 0;
	}
	
    return (
		
		<div className="page">
			<div className="order-cont">
				<div className="products-cont">
					<h4>{storeName}</h4>
					<span className="line" />
					{productsInCart.length !== 0 ? (
						productsInCart.map((product) => (
							<CartProduct
								key={product.id}
								product={product}
								quantity={getQuanOfProduct(product.id)}
								onRemove={onRemove}
								propHandleDelete={propHandleDelete}
                                propHandleAdd={(product:Product)=>propHandleAdd(product,storeID)}
                                changeQuantity={(productID,newQuantity)=>changeQuantity(storeID,productID,newQuantity)}
                               
							/>
						))
					) : (
						<>
							<h4 className="empty-bag-msg">Your bag is empty</h4>
							<h5>
								You can find products to purchase at the <Link to="/">store</Link>{' '}
							</h5>
						</>
					)}
				</div>
				<div className="summary-cont">
					<h4>Order Summary</h4>
					<span className="line" />
					<div className="total-price">
						<h4>Total:</h4>
						<h4>{total}$</h4>
					</div>
					{/* <Button variant="contained" color="secondary" startIcon={<PurchaseIcon />}>
						Checkout
					</Button> */}
				</div>
			</div>
		</div>
	);
}

export default Bag;
