import { Button, Card, CardContent, Typography } from '@material-ui/core';
import React, {FC,useEffect,useRef} from 'react';
import '../styles/ProductSearch.scss';
import { Link } from 'react-router-dom';
import useAPI from '../hooks/useAPI';
import {Store} from '../types';



type ProductSearchProps = {
    content:string,
    price:number,
    storeID:string,
    quantity:number,
    clickAddProduct:()=>void,
};

const ProductSearch: FC<ProductSearchProps> = ({storeID,content,price,quantity,clickAddProduct}) => {

    const storeName = useRef<string>("")

    const storeObj = useAPI<Store>('/get_store',{store_id:storeID});
    useEffect(()=>{
        storeObj.request().then(({data,error,errorMsg})=>{
            if(!error && data !==null){
                storeName.current = data.data.name;
            }
            else{
                alert(errorMsg)
            }
            
        })
    },[]);

	return (
		<div className="ProductSearchCard">
            
            {content!==""?
                <Card 
                    className="prodCard"
                    style={{
                        backgroundColor: "#83f1e8",
                    }}
                    >
                    <CardContent className="cardContent">
                        <Typography style={{'fontSize':'large','fontWeight':'bold'}}>
                            {content}
                        </Typography> 
                        <Typography style={{'marginTop':'5%'}}>
                            {price}$
                        </Typography> 
                        <Typography style={{'marginTop':'5%'}}>
                            Quantity: {quantity}
                        </Typography> 
                    </CardContent>
                    <div className="buttonLink">
                        <Button 
                            style={{
                                'color':'blue',
                                'background':'#ffffff',
                                'marginTop':'10%'
                            }}
                            onClick = {()=>clickAddProduct()}    
                        >
                        Add To Cart
                        </Button>
                        <Link 
                            className="linkStore"
                            to={{
                            pathname: '/storesView',
                            state: {
                                storeID:storeID
                            },
                            }}
                        >
                                {storeName.current}
                        </Link>
                    </div>
                </Card>
            :null}
		</div>
	);
};
export default ProductSearch;
