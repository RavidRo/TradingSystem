import { Button, Card, CardContent, Typography } from '@material-ui/core';
import React, {FC} from 'react';
import { Route } from 'react-router';
import StoresView from '../pages/StoresView';
import '../styles/ProductSearch.scss';
import { Link } from 'react-router-dom';



type ProductSearchProps = {
    content:string,
    price:number,
    id:number,
    storeName:string,
    clickAddProduct:()=>void,
};

const ProductSearch: FC<ProductSearchProps> = ({id,storeName,content,price,clickAddProduct}) => {

      
	return (
		<div className="ProductSearchCard">
            {content!==""?
                <Card 
                    className="prodCard"
                    style={{
                        backgroundColor: "#83f1e8",
                        width:'350px',
                        height:'200px',
                
                    }}
                    >
                    <CardContent className="cardContent">
                        <Typography style={{'fontSize':'large','fontWeight':'bold'}}>
                            {content}
                        </Typography> 
                        <Typography style={{'marginTop':'5%'}}>
                            {price}$
                        </Typography> 
                        <Typography style={{'marginTop':'1%'}}>
                            {storeName}
                        </Typography> 
                    </CardContent>
                    <div className="buttonLink">
                        <Button 
                            style={{
                                'color':'blue',
                                'marginTop':'10%',
                                'background':'#ffffff',
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
                                storeName:storeName
                            },
                            }}
                            // style={{
                            //     'color':'blue',
                            //     'marginLeft':'25%',
                            //     'marginTop':'200px'
                            // }}
                        >
                                Go To Store
                        </Link>
                    </div>
                </Card>
            :null}
		</div>
	);
};
export default ProductSearch;
