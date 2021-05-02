import React, { FC, useState , useEffect} from 'react';
import '../styles/Cart.scss';
import Bag from '../components/Bag';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@material-ui/core';
import { Link } from 'react-router-dom';
import storesProductsMap from '../components/storesProductsMap';
import {Product,ProductQuantity} from '../types';
import useAPI from '../hooks/useAPI';

type CartProps = {
	products:ProductQuantity[],
    handleDeleteProduct:(product:Product|null)=>void,

};

const Cart: FC<CartProps> = ({products,handleDeleteProduct}) => {
	const [productsInCart,setProducts] = useState<ProductQuantity[]>(products);
    const [open,setOpen] = useState<boolean>(false);
    const [age,setAge] = useState<number>(0);
    const [showPurchaseLink,setLink] = useState<boolean>(false);

    const calculateTotal = ()=>{
		const reducer = (accumulator:number, currentValue:ProductQuantity) => accumulator + (currentValue.price*currentValue.quantity);
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

    const getProduct = (id:string)=>{
        for(var i=0;i<productsInCart.length;i++){
            if(productsInCart[i].id===id){
                return {
                    id:id,
                    name:productsInCart[i].name,
                    price:productsInCart[i].price,
                    category:productsInCart[i].category,
                    keywords:productsInCart[i].keywords
                }
            }
        }
        return null;
    }

	const handleDeleteProductMy = (id:string)=>{
		setProducts(productsInCart.filter((product) => product.id !== id));
        setTotalAmount(calculateTotal());
        handleDeleteProduct(getProduct(id));
	}
    const productUpdateObj = useAPI<Product[]>('/change_product_quantity_in_cart',{},'POST');
    const changeQuantity = (id: string, newQuantity: number)=>{
        productsInCart.forEach((product) => {
			if (product.id === id) {
				product.quantity = newQuantity;
			}
		});
        setTotalAmount(calculateTotal());
        productUpdateObj.request({store_id:findBagByProductID(id),product_id:id,quantity:newQuantity}).then(({data,error,errorMsg})=>{
            if(!productUpdateObj.error && productUpdateObj.data!==null){
                // do nothing
                void(0);
            }
        })
    }
    const discountObj = useAPI<number>('/get_discount',{age:age});
    useEffect(()=>{
        discountObj.request().then(({data,error,errorMsg})=>{
            if(!discountObj.error && discountObj.data!==null){
                setTotalAmount(discountObj.data);
            }
            
        })
    },[showPurchaseLink]);
    
    const handleOK = ()=>{
        setOpen(false);
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
                propHandleDelete={handleDeleteProductMy}
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
