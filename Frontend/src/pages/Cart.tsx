import React, { FC, useState , useEffect,useRef} from 'react';
import '../styles/Cart.scss';
import Bag from '../components/Bag';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@material-ui/core';
import { Link } from 'react-router-dom';
import {Product,ProductQuantity,ShoppingCart,ShoppingBag,ProductToQuantity} from '../types';
import useAPI from '../hooks/useAPI';
import { faShoppingBag } from '@fortawesome/free-solid-svg-icons';

type CartProps = {
	products:ProductQuantity[],
    handleDeleteProduct:(product:Product|null)=>void,

};

const Cart: FC<CartProps> = ({products,handleDeleteProduct}) => {
    const [open,setOpen] = useState<boolean>(false);
    const [age,setAge] = useState<number>(0);
    const [showPurchaseLink,setLink] = useState<boolean>(false);
    const [bagsToProducts,setBags] = useState<ShoppingBag[]>([]);

    const cartObj = useAPI<ShoppingCart>('/get_cart_details');
    useEffect(()=>{
        cartObj.request().then(({data,error,errorMsg})=>{
                
            if(!error && data!==null){
                console.log(data.data);
                setBags(data.data.bags);
            }
            else{
                alert(errorMsg)
            }
        })
    },[]);


    const productQuantityOfTuples = (bag:ShoppingBag)=>{
        let bagIndex:number = bagsToProducts.indexOf(bag);
        let tupleArr:ProductToQuantity[] = bagsToProducts[bagIndex].prodQuantities;
        let prodQuantities:ProductQuantity[] = tupleArr.map(tuple=>{
                                                            return {
                                                                id:tuple[0].id,
                                                                name:tuple[0].name,
                                                                category:tuple[0].category,
                                                                price:tuple[0].price,
                                                                keywords:tuple[0].keywords,
                                                                quantity:tuple[1]}})
         return prodQuantities;           

    }
    const calculateTotal = ()=>{
        let total = 0;
        for(var i=0;i<bagsToProducts.length;i++){
            let priceBag:number = 0;
            for(var j=0;j<bagsToProducts[i].prodQuantities.length;j++){
                let productPrice:number = bagsToProducts[i].prodQuantities[j][0].price;
                let productQuantity = bagsToProducts[i].prodQuantities[j][1];
                priceBag+= productPrice* productQuantity;
            }
            total+=priceBag;
        }
        return total;
	}
    const [totalAmount,setTotalAmount] = useState<number>(calculateTotal());

   
	const handleDeleteProductMy = (id:string)=>{
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
        setTotalAmount(calculateTotal());
        handleDeleteProduct(product);
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
        setTotalAmount(calculateTotal());

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
    const discountObj = useAPI<number>('/get_discount',{age:age});
    useEffect(()=>{
        if(showPurchaseLink){
            discountObj.request().then(({data,error,errorMsg})=>{
                if(!error && data!==null){
                    setTotalAmount(data.data);
                }
                else{
                    alert(errorMsg)
                }
                
            })
        }
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
            {bagsToProducts.map((bag)=>{
                return (
                <Bag
                key={bagsToProducts.indexOf(bag)}
                storeName={bag.storeName}
                products={productQuantityOfTuples(bag)}
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
