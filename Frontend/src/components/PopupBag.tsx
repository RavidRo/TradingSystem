
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React ,{FC, useEffect, useState, useRef} from 'react';
import ProductPopup from '../components/ProductPopup';
import {Product,ProductQuantity,Store} from '../types';
import useAPI from '../hooks/useAPI';

type PopupBagProps = {
    storeID:string,
    products:ProductQuantity[],
    propHandleDelete:(productID:string)=>void,
    propHandleAdd:(product:Product,storeID:string)=>Promise<boolean>;

   
};
const PopupBag: FC<PopupBagProps> = ({storeID,products,propHandleAdd,propHandleDelete}:PopupBagProps) => {

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
    })},[]);

    return (
		
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
                                propHandleAdd={(product:Product)=>propHandleAdd(product,storeID)}
                                key={Object.values(productsInCart).indexOf(p)}
                                />
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
            </h3>
            
		</div>
	);
}

export default PopupBag;
