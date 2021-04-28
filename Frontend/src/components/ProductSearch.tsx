import { Button, Card, CardContent } from '@material-ui/core';
import React, { useState, FC} from 'react';
import '../styles/ProductSearch.scss';



type ProductSearchProps = {
    content:string,
    clickAddProduct:()=>void,
};

const ProductSearch: FC<ProductSearchProps> = ({content,clickAddProduct}) => {

      
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
                            {content}
                    </CardContent>
                        <Button 
                            style={{
                                'color':'blue',
                                'marginTop':'20%',
                                'background':'#ffffff',
                            }}
                            onClick = {()=>clickAddProduct()}    
                        >
                        Add To Cart
                        </Button>
                </Card>
            :null}
		</div>
	);
};
export default ProductSearch;
