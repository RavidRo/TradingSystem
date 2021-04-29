import React, { FC, useState , useEffect} from 'react';
import '../styles/Cart.scss';
import Bag from '../components/Bag';
import storesProductsMap from '../components/storesProductsMap';
import { Button } from '@material-ui/core';
import { Link } from 'react-router-dom';


type CartProps = {
	products:{id:string,name:string,price:number,quantity:number}[],

};

const Cart: FC<CartProps> = ({products}) => {
	const [productsInCart,setProducts] = useState<{id:string,name:string,price:number,quantity:number}[]>(products);
    const findBagByProductID = (id:string)=>{
        for(var i=0; i<Object.keys(storesProductsMap).length;i++){
            let productsArray = (Object.values(storesProductsMap)[i]);
            for(var j=0; j<productsArray.length;j++){
                if(productsArray[j].id===id){
                    // return store name
                    return Object.keys(storesProductsMap)[i];
                }
            }
        }
        return "";
    }
    const bagsInclude = (storeName:string ,array:any[])=>{
        for(var i=0; i<Object.keys(array).length; i++){
            if(Object.keys(array[i])[0]===storeName){
                return true;
            }
        }
        return false;
    }
    const bagsIndexOf = (storeName:string ,array:any[])=>{
        for(var i=0; i<array.length; i++){
            if(Object.keys(array[i])[0]===storeName){
                return i;
            }
        }
        return -1;
    }
	const setProductsInBags = ()=>{
        let bagsArray:any = [];
        for(var i=0; i<Object.keys(productsInCart).length; i++){
            let storeName = findBagByProductID(Object.values(productsInCart)[i].id);
            if(storeName!==""){
                if(bagsInclude(storeName,bagsArray)){
                    let indexOfStore = bagsIndexOf(storeName,bagsArray);
                    bagsArray[indexOfStore][storeName].push(productsInCart[i]);
                }
                else{
                    var storeProduct:any = {};
                    storeProduct[storeName] = [productsInCart[i]];
                    bagsArray.push(storeProduct)
                }
            }
            else{
                alert((productsInCart)[i]);
            }
        }
        return bagsArray;

    }

    useEffect(()=>{
        setProducts(products);
        setBags(setProductsInBags());
    },[products]);
	const [bags,setBags] = useState<any[]>(setProductsInBags());

	const handleDeleteProduct = (product:{id:string,name:string,price:number})=>{

	}

	return (
		<div className="cart">
            <h3 className="cartTitle">
                My Cart:
            </h3>
            {bags.map((bag)=>{
                let storeName = Object.keys(bag)[0];
                let index=bagsIndexOf(storeName,bags);
                return (
                <Bag
                key={index}
                storeName={storeName}
                products={bag[storeName]}
                propHandleDelete={handleDeleteProduct}
                />)
                    
            })}
             <Link 
                className="link" 
                to={{
                pathname: '/Purchase',
                state: {
                   
                },
                }}>
                <Button className="purchaseBtn" style={{background:'rgb(255, 229, 80)',height:'50px',fontWeight:'bold',fontSize:'large'}}>
                    Purchase Cart
                </Button>
            </Link>
            
            
		</div>
	);
};

export default Cart;
