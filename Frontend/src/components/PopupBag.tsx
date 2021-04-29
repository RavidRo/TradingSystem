
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React ,{FC, useEffect, useState} from 'react';
import ProductPopup from '../components/ProductPopup';

type PopupBagProps = {
    storeName:string,
    products:{id:number, name:string,price:number,quantity:number}[],
    propHandleDelete:(product:{id:number,name:string,price:number})=>void,
   
};
const PopupBag: FC<PopupBagProps> = ({storeName,products,propHandleDelete}:PopupBagProps) => {

    const [productsInCart,setProducts] = useState<{id:number,name:string,price:number,quantity:number}[]>(products);
	
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
                                propHandleDelete={propHandleDelete}
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
