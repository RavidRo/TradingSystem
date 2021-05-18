
import React ,{FC, useEffect, useState,useRef} from 'react';
import '../styles/PopupCart.scss';
import PopupBag from '../components/PopupBag';
import {Product,ProductQuantity,ShoppingBag,ShoppingCart,ProductToQuantity,StoreToSearchedProducts,Store} from '../types';
import useAPI from '../hooks/useAPI';

type PopupCartProps = {
    products:ProductQuantity[],
    storesToProducts:StoreToSearchedProducts,
    propHandleDelete:(product:Product,storeID:string)=>Promise<boolean> | boolean,
    changeQuantity:(store:string,product:string,quan:number)=>Promise<boolean>;
    propUpdateStores:(map:StoreToSearchedProducts)=>void,
};
const PopupCart: FC<PopupCartProps> = ({products,storesToProducts,propHandleDelete,changeQuantity,propUpdateStores}: PopupCartProps) => {

    const [storesToProductsMy,setStoresProducts] = useState<StoreToSearchedProducts>(storesToProducts);

    //helper function to present the products and give the to bag nicely
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
    //need to delete product from cart and update the server
    const handleDeleteProductMy = (product:Product,bagID:string)=>{
        let answer = propHandleDelete(product,bagID);//update the server
        if(answer !== false && answer !== true){
            answer.then((result)=>{
                if(result===true){
                    for(var i=0;i<Object.keys(storesToProductsMy).length;i++){
                        let tupleArr = Object.values(storesToProductsMy)[i];
                        for(var j=0;j<tupleArr.length;j++){
                            if(tupleArr[j][0].id===product.id){
                                // change product quantity in bag to 0
                                tupleArr[j][1]=0;
                                Object.values(storesToProductsMy)[i] = tupleArr;
                            }
                        }
                    }
                }
            })
        }
        
        return answer;
	}
    //load the cart when user enters the website
    const cartObj = useAPI<ShoppingCart>('/get_cart_details');
    const productObj = useAPI<Product>('/get_product');
    useEffect(()=>{
        cartObj.request().then(({data,error,errorMsg})=>{
            if(!error && data!==null){
                let bags = data.data.bags;
                let map:{[storeID:string]: ProductToQuantity[]} = {};
                let promises : Promise<void>[] =  [];
                for(var i=0;i<bags.length;i++){
                    let bag = bags[i];
                    let storeID = bag.store_id;
                    let productQuantitiesMap = bag.product_ids_to_quantities;
                    let tuplesArr: ProductToQuantity[] = [];
                    for(var j=0; j<Object.keys(productQuantitiesMap).length; j++){
                        let productID:string = Object.keys(productQuantitiesMap)[j];
                        let quantity:number = Object.values(productQuantitiesMap)[j];

                        let promise = productObj.request({product_id: productID, store_id: storeID}).then(({data, error, errorMsg})=>{
                            if(!error && data!==null){
                                let product = data.data;
                                tuplesArr.push([product, quantity])
                            }
                            else{
                                alert(errorMsg);
                            }
                        });
                        promises.push(promise);  
                    }
                    map[storeID] = tuplesArr;
                }
                Promise.allSettled(promises).then(()=>{
                    setStoresProducts(map);
                    propUpdateStores(map);
                })
                
            }
            else{
                alert(errorMsg)
            }
        })
    },[storesToProducts, products]);

    return (
		
		<div className="popupCart">
            {Object.keys(storesToProductsMy).map((bagID)=>{
                return (
                <PopupBag
                key={bagID}
                storeID={bagID}
                products={productQuantityOfTuples(storesToProductsMy[bagID])}
                propHandleDelete={(product:Product)=>handleDeleteProductMy(product,bagID)}
                changeQuantity={changeQuantity}
                />
                )
                    
            })}
            
		</div>
	);
}

export default PopupCart;
