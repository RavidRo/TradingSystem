import { Button, Card, CardContent, Typography } from '@material-ui/core';
import React, {FC} from 'react';
import '../styles/ProductSearch.scss';



type ProductSearchProps = {
    content:string,
    price:number,
    clickAddProduct:()=>void,
};

const ProductSearch: FC<ProductSearchProps> = ({content,price,clickAddProduct}) => {

      
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
                    </CardContent>
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
                </Card>
            :null}
		</div>
	);
};
export default ProductSearch;
