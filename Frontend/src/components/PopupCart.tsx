
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow } from '@material-ui/core';
import React ,{FC, useEffect, useState} from 'react';
import '../styles/PopupCart.scss';
import ProductPopup from '../components/ProductPopup';
import storesProductsMap from '../components/storesProductsMap';
import PopupBag from '../components/PopupBag';

type PopupCartProps = {
    products:{id:number,name:string,price:number,quantity:number}[],
    propHandleDelete:(product:{id:number,name:string,price:number})=>void,
   
};
const PopupCart: FC<PopupCartProps> = ({products,propHandleDelete}: PopupCartProps) => {

    const findBagByProductID = (id:number)=>{
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

    const [productsInCart,setProducts] = useState<{id:number,name:string,price:number,quantity:number}[]>(products);
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
            {/* <TableContainer>
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
            </TableContainer> */}
            
		</div>
	);
}

export default PopupCart;
