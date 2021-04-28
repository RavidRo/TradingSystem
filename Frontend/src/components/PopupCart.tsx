
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React ,{FC, useEffect, useState} from 'react';
import '../styles/PopupCart.scss';
import ProductPopup from '../components/ProductPopup';

type PopupCartProps = {
    products:{name:string,price:number,quantity:number}[],
    propHandleDelete:(product:{name:string,price:number})=>void,
   
};
const PopupCart: FC<PopupCartProps> = ({products,propHandleDelete}: PopupCartProps) => {

    const [productsInCart,setProducts] = useState<{name:string,price:number,quantity:number}[]>(products);
	
    useEffect(()=>{
        setProducts(products);
    },[products]);


    return (
		
		<div className="popupCart">
            
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
            
		</div>
	);
}

export default PopupCart;
