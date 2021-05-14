import React, { FC, useState , useEffect,useRef} from 'react';
import '../styles/Cart.scss';
import Bag from '../components/Bag';
import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, TextField } from '@material-ui/core';
import { Link } from 'react-router-dom';
import {Product,ProductQuantity,ShoppingCart,ShoppingBag,ProductToQuantity,StoreToSearchedProducts} from '../types';
import useAPI from '../hooks/useAPI';

type CartProps = {
	products:ProductQuantity[],
    storesToProducts:StoreToSearchedProducts,
    handleDeleteProduct:(product:Product|null,storeID:string)=>void,
    propHandleAdd:(product:Product,storeID:string)=>Promise<boolean>;
    changeQuantity:(store:string,product:string,quan:number)=>void;
    getPropsCookie:()=>string,
};

const Cart: FC<CartProps> = ({products,storesToProducts,handleDeleteProduct, propHandleAdd, changeQuantity, getPropsCookie}) => {
    const [open,setOpen] = useState<boolean>(false);
    const [age,setAge] = useState<number>(0);
    const [showPurchaseLink,setLink] = useState<boolean>(false);
    const [bagsToProducts,setBags] = useState<ShoppingBag[]>([]);
    const [storesToProductsMy,setStoresProducts] = useState<StoreToSearchedProducts>(storesToProducts);

    useEffect(()=>{
        console.log(storesToProducts);
        setStoresProducts(storesToProducts);
        setTotalAmount(calculateTotal());
    },[storesToProducts]);

    const cartObj = useAPI<ShoppingCart>('/get_cart_details');
    useEffect(()=>{
        cartObj.request().then(({data,error,errorMsg})=>{
                
            if(!error && data!==null){
                setBags(data.data.bags);
            }
            else{
                alert(errorMsg)
            }
        })
    },[]);


    const productQuantityOfTuples = (bagID:string)=>{
        let productsToReturn = [];
        let tuples = storesToProducts[bagID];
        for(var i=0;i<tuples.length; i++){
            let product = {
                id: tuples[i][0].id,
                name: tuples[i][0].name,
                price: tuples[i][0].price,
                category: tuples[i][0].category,
                keywords: tuples[i][0].keywords,
                quantity: tuples[i][1]
            }
            productsToReturn.push(product);
        }
        return productsToReturn;

    }

    const calculateTotal = ()=>{
        let total = 0;
        for(var i=0;i<Object.keys(storesToProductsMy).length;i++){
            let priceBag:number = 0;
            for(var j=0;j<Object.values(storesToProductsMy)[i].length;j++){
                let productPrice:number = Object.values(storesToProductsMy)[i][j][0].price;
                let productQuantity = Object.values(storesToProductsMy)[i][j][1];
                priceBag+= productPrice* productQuantity;
            }
            total+=priceBag;
        }
        return total;
	}
    const [totalAmount,setTotalAmount] = useState<number>(calculateTotal());

   
	const handleDeleteProductMy = (id:string,storeID:string)=>{
        let product:Product= {} as Product;
        for(var i=0;i<Object.keys(storesToProductsMy).length;i++){
            let tupleArr = Object.values(storesToProductsMy)[i];
            for(var j=0;j<tupleArr.length;j++){
                if(tupleArr[i][0].id===id){
                    product=Object.values(storesToProductsMy)[i][j][0];
                    // change product quantity in bag to 0
                    tupleArr[i][1]=0;
                    Object.values(storesToProductsMy)[i] = tupleArr;
                }
            }
        }
        setTotalAmount(calculateTotal()); //updating amount
        handleDeleteProduct(product,storeID); //updating server
	}

    const changeQuantityMy = (storeID: string, prodID:string,  newQuantity: number)=>{
        for(var i=0;i<Object.keys(storesToProductsMy).length;i++){
            let tuplesArr = Object.values(storesToProductsMy)[i];
            for(var j=0;j<tuplesArr.length;j++){
                    if(tuplesArr[j][0].id===prodID){
                        Object.values(storesToProductsMy)[i][j][1]=newQuantity;
                    }
                }
            }
        changeQuantity(storeID,prodID,newQuantity);//update server
        setTotalAmount(calculateTotal());

    }
    const discountObj = useAPI<number>('/purchase_cart',{cookie: getPropsCookie(), age:age}, 'POST');
    useEffect(()=>{
        if(showPurchaseLink){
            discountObj.request().then(({data,error,errorMsg})=>{
                if(!error && data!==null){
                    let prevCost = totalAmount;
                    if(data.data < prevCost){
                        alert("Congratulations! You got discount of: "+ (prevCost - data.data));
                        setTotalAmount(data.data);
                    }
                    else{
                        alert("No discount for you :(");
                    }
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

    const updateAmount = (product:Product)=>{
        let newAmount = totalAmount;
        newAmount = newAmount + (product.price);
        setTotalAmount(newAmount);
    }

    const handleAddMy = (product:Product,storeID:string)=>{
        updateAmount(product);
        return propHandleAdd(product,storeID);
    }

	return (
		<div className="cart">
            <h3 className="cartTitle">
                My Cart:
            </h3>
            {Object.keys(storesToProductsMy).map((bagID)=>{
                return (
                <Bag
                key={bagID}
                storeID={bagID}
                products={productQuantityOfTuples(bagID)}
                propHandleDelete={(productID:string)=>handleDeleteProductMy(productID,bagID)}
                propHandleAdd={(product:Product,storeID:string)=>handleAddMy(product,storeID)}
                changeQuantity={(storeID, productID, newQuantity)=>changeQuantityMy(storeID, productID,newQuantity)}
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
