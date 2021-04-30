import { Button, Card, CardContent, Typography } from '@material-ui/core';
import React, {FC} from 'react';
import '../styles/ProductSearch.scss';
import { Link } from 'react-router-dom';



type ProductSearchProps = {
    content:string,
    price:number,
    id:string,
    storeID:string,
    clickAddProduct:()=>void,
};

const ProductSearch: FC<ProductSearchProps> = ({id,storeID,content,price,clickAddProduct}) => {

      
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
                                {storeID}
                        </Link>
                    </div>
                </Card>
            :null}
		</div>
	);
};
export default ProductSearch;
