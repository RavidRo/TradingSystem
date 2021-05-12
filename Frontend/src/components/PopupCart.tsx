
import React ,{FC, useEffect, useState,useRef} from 'react';
import '../styles/PopupCart.scss';
import storesProductsMap from '../components/storesProductsMap';
import PopupBag from '../components/PopupBag';
import {Product,ProductQuantity,ShoppingBag,ShoppingCart,ProductToQuantity,StoreToSearchedProducts,Store} from '../types';
import useAPI from '../hooks/useAPI';

type PopupCartProps = {
    products:ProductQuantity[],
    storesToProducts:StoreToSearchedProducts,
    propHandleDelete:(product:Product,storeID:string)=>void,
	propHandleAdd:(product:Product,storeID:string)=>Promise<boolean>;
   
};
const PopupCart: FC<PopupCartProps> = ({products,propHandleAdd,storesToProducts,propHandleDelete}: PopupCartProps) => {

    const [bagsToProducts,setShoppingBags] = useState<ShoppingBag[]>([]);

    const [storesToProductsMy,setStoresProducts] = useState<StoreToSearchedProducts>(storesToProducts);

    const productQuantityOfTuples = (tuples:ProductToQuantity[])=>{
        let prodQuantities:ProductQuantity[] = tuples.map(tuple=>{
                                                            return {
                                                                id:tuple[0].id,
                                                                name:tuple[0].name,
                                                                category:tuple[0].category,
                                                                price:tuple[0].price,
                                                                keywords:tuple[0].keywords,
                                                                quantity:tuple[1]}})
         return prodQuantities;           

    }
    const handleDeleteProductMy = (id:string,bagID:string)=>{
        let product:Product= {} as Product;
        for(var i=0;i<bagsToProducts.length;i++){
            for(var j=0;j<bagsToProducts[i].prodQuantities.length;j++){
                if(bagsToProducts[i].prodQuantities[j][0].id===id){
                    product=bagsToProducts[i].prodQuantities[j][0];
                    // change product quantity in bag to 0
                    bagsToProducts[i].prodQuantities[j][1] = 0;
                }
            }
        }
        propHandleDelete(product,bagID);
	}
    const findBagByProductID = (productID:string)=>{
        for(var i=0;i<bagsToProducts.length;i++){
            for(var j=0;j<bagsToProducts[i].prodQuantities.length;j++){
                if(bagsToProducts[i].prodQuantities[j][0].id===productID){
                    return bagsToProducts[i].storeID;
                }
            }
        }
    }
    const productUpdateObj = useAPI<void>('/change_product_quantity_in_cart',{},'POST');
    const changeQuantity = (id: string, newQuantity: number)=>{
        for(var i=0;i<bagsToProducts.length;i++){
            for(var j=0;j<bagsToProducts[i].prodQuantities.length;j++){
                if(bagsToProducts[i].prodQuantities[j][0].id===id){
                    // change product quantity in bag to newQuantity
                    bagsToProducts[i].prodQuantities[j][1] = newQuantity;
                }
            }
        }

        productUpdateObj.request({store_id:findBagByProductID(id),product_id:id,quantity:newQuantity}).then(({data,error,errorMsg})=>{
            if(!error && data!==null){
                // do nothing
                void(0);
            }
            else{
                alert(errorMsg);
            }
        })
    }
 
    
    const bagIDToName = useRef<{[storeID: string]: ShoppingBag}>({});
    const cartObj = useAPI<ShoppingCart>('/get_cart_details');
    useEffect(()=>{
        cartObj.request().then(({data,error,errorMsg})=>{
            if(!error && data!==null){
                let bags = data.data.bags;
                for(var i=0;i<bags.length;i++){
                    bagIDToName.current[bags[i].storeID] = bags[i];
                }
                setShoppingBags(data.data.bags);
            }
            else{
                alert(errorMsg)
            }
        })
    },[]);

    return (
		
		<div className="popupCart">
            {Object.keys(storesToProductsMy).map((bagID)=>{
                return (
                <PopupBag
                key={bagID}
                storeID={bagID}
                products={productQuantityOfTuples(storesToProductsMy[bagID])}
                propHandleDelete={(productID:string)=>handleDeleteProductMy(productID,bagID)}
                propHandleAdd={propHandleAdd}
                />)
                    
            })}
            
		</div>
	);
}

export default PopupCart;
