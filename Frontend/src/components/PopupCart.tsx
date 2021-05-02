
import React ,{FC, useEffect, useState} from 'react';
import '../styles/PopupCart.scss';
import storesProductsMap from '../components/storesProductsMap';
import PopupBag from '../components/PopupBag';
import {Product} from '../types';

type PopupCartProps = {
    products:Product[],
    propHandleDelete:(product:Product)=>void,
   
};
const PopupCart: FC<PopupCartProps> = ({products,propHandleDelete}: PopupCartProps) => {

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

    const [productsInCart,setProducts] = useState<Product[]>(products);
    const [bags,setBags] = useState<any[]>(setProductsInBags());

    useEffect(()=>{
        setProducts(products);
        setBags(setProductsInBags());
    },[products]);



    return (
		
		<div className="popupCart">
            {bags.map((bag)=>{
                let storeName = Object.keys(bag)[0];
                let index=bagsIndexOf(storeName,bags);
                return (
                <PopupBag
                key={index}
                storeName={storeName}
                products={bag[storeName]}
                propHandleDelete={propHandleDelete}
                />)
                    
            })}
            
		</div>
	);
}

export default PopupCart;
