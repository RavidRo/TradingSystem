
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React ,{FC, useEffect, useState} from 'react';
import ProductPopup from '../components/ProductPopup';
import {Product,ProductQuantity} from '../types';

type PopupBagProps = {
    storeName:string,
    storeID:string,
    products:ProductQuantity[],
    propHandleDelete:(product:ProductQuantity)=>void,
    propHandleAdd:(product:Product,storeID:string)=>void;

   
};
const PopupBag: FC<PopupBagProps> = ({storeName,storeID,products,propHandleAdd,propHandleDelete}:PopupBagProps) => {

    const [productsInCart,setProducts] = useState<ProductQuantity[]>(products);
	
    useEffect(()=>{
        setProducts(products);
    },[products]);


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
