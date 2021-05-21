
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React ,{FC, useEffect, useState} from 'react';
import ProductPopup from '../components/ProductPopup';
import {Product,ProductQuantity,Store} from '../types';
import useAPI from '../hooks/useAPI';

type PopupBagProps = {
    storeID:string,
    products:ProductQuantity[],
    propHandleDelete:(product:Product)=>Promise<boolean> | boolean,
    changeQuantity:(store:string,product:string,quan:number)=>Promise<boolean>,

   
};
const PopupBag: FC<PopupBagProps> = ({storeID,products,propHandleDelete,changeQuantity}:PopupBagProps) => {

    const [productsInCart,setProducts] = useState<ProductQuantity[]>(products);
    const [storeName,setStoreName] =  useState<string>("");
	
    useEffect(()=>{
        setProducts(products);
    },[products]);

    const storeIDToNameObj = useAPI<Store>('/get_store',{store_id:storeID});
    useEffect(()=>{
        storeIDToNameObj.request().then(({ data, error, errorMsg }) => {
            if (!error && data !== null) {
                setStoreName(data.data.name);
            }
            else{
                alert(errorMsg);
            }
    // eslint-disable-next-line react-hooks/exhaustive-deps
    })},[]);

    const shouldPresent = ()=>{
        for(var i=0; i<productsInCart.length; i++){
            if(productsInCart[i].quantity>0){
                return true;
            }
        }
        return false; //all products in cart have quantity 0
    }
   
 

    return (
        shouldPresent()?
		<div className="PopupBag">
            <h3>
                {storeName}
                <TableContainer>
                    <Table  aria-label="simple table">
                        <TableHead className="tableHead">
                            <TableRow>
                                <TableCell align={'center'}>Product</TableCell>
                                <TableCell align={'center'}>Price</TableCell>
                                <TableCell align={'center'}>Quantity</TableCell> 
                                <TableCell></TableCell>
                            </TableRow>
                        </TableHead>
                        
                        <TableBody>
                            {Object.values(productsInCart).map((p) => (
                                <ProductPopup
                                id={p.id}
                                name={p.name}
                                price={p.price}
                                quantity = {p.quantity}
                                keywords={p.keywords}
                                category={p.category}
                                propHandleDelete={propHandleDelete}
                                changeQuantity={(productID,newQuantity)=>changeQuantity(storeID,productID,newQuantity)}
                                key={Object.values(productsInCart).indexOf(p)}
                                />
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </h3>
            
		</div>
        :null
	);
}

export default PopupBag;
