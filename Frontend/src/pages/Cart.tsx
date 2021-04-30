import React, { FC, useState , useEffect} from 'react';
import '../styles/Cart.scss';
import Bag from '../components/Bag';
import storesProductsMap from '../components/storesProductsMap';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@material-ui/core';
import { Link } from 'react-router-dom';

type CartProps = {
	products:{id:string,name:string,price:number,quantity:number}[],

};
type Product = {
	id:string,
    name:string,
    price: number,
    quantity:number
}
const Cart: FC<CartProps> = ({products}) => {
	const [productsInCart,setProducts] = useState<{id:string,name:string,price:number,quantity:number}[]>(products);
    const [open,setOpen] = useState<boolean>(false);
    const [age,setAge] = useState<number>(0);
    const [showPurchaseLink,setLink] = useState<boolean>(false);

    const calculateTotal = ()=>{
		const reducer = (accumulator:number, currentValue:Product) => accumulator + (currentValue.price*currentValue.quantity);
        return productsInCart.reduce(reducer,0);
	}
    const [totalAmount,setTotalAmount] = useState<number>(calculateTotal());

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

	const handleDeleteProduct = (id:string)=>{
		setProducts(productsInCart.filter((product) => product.id !== id));
        setTotalAmount(calculateTotal());
	}
    const changeQuantity = (id: string, newQuantity: number)=>{
        productsInCart.forEach((product) => {
			if (product.id === id) {
				product.quantity = newQuantity;
			}
		});
        setTotalAmount(calculateTotal());
    }
   
    const handleOK = ()=>{
        setOpen(false);

        // TODO: ask from server for discount with age
        // setTotal(from server)
        setLink(true);
    }
    const handleClick = ()=>{
        setOpen(true);
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
                changeQuantity={changeQuantity}
                />)
                    
            })}
                 <h3 className="totalAmount">
                    Total amount : {totalAmount}
                </h3>
                <Button 
                    className="purchaseBtn" 
                    style={{
                        height:'50px',
                        fontWeight:'bold',
                        fontSize:'large',
                        border: '#00ffff',
                        borderWidth: '4px',
                        borderStyle:'solid'
                    }}
                    onClick={handleClick}
                > 
                Enter Your Age For Discount
                </Button>
                <Dialog open={open} onClose={()=>setOpen(false)} aria-labelledby="form-dialog-title">
                <DialogTitle  id="form-dialog-title">Enter Your Age</DialogTitle>
                <DialogContent>
                <DialogContentText style={{'fontSize':'20px','color':'black'}}>
                    See if there is a discount available for you
                </DialogContentText>
                <TextField
                    autoFocus
                    margin="dense"
                    id="age"
                    label="Age"
                    type="number"
                    fullWidth
                    onChange={(e)=>setAge(+e.target.value)}
                />
                </DialogContent>
                <DialogActions>
                <Button style={{'color':'blue'}} onClick={()=>setOpen(false)} >
                    Cancel
                </Button>
                <Button style={{'color':'blue'}} onClick={()=>handleOK()}>
                    OK
                </Button>
                </DialogActions>
            </Dialog>
            {showPurchaseLink?
                <Link 
                        className="link" 
                        to={{
                        pathname: '/Purchase',
                        state: {
                            totalAmount:totalAmount
                        },
                        }}
                    >
                    <button 
                    className="purchaseBtn" 
                    style={{background:'#7FFF00',height:'50px',fontWeight:'bold',fontSize:'large',marginTop:'40%',marginLeft:'20%'}}
                    onClick={handleClick}
                    > 
                    Purchase
                    </button>
                </Link>   
            :null}
        </div> 
            
	);
};

export default Cart;
