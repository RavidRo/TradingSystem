import { Button, Card, CardContent } from '@material-ui/core';
import React, { useState, FC} from 'react';
import '../styles/SearchPage.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons';
import ProductSearch from '../components/ProductSearch';
import FilterMenu from '../components/FilterMenu';
import SearchCategory from '../components/SearchCategory';

type SearchPageProps = {
    location: any,
};

const SearchPage: FC<SearchPageProps> = ({location}) => {
    const [searchProduct, setSearchProduct] = useState<string>(location.state.product);
    
    const [fromInput, setFromInput] = useState<number>(0);
    const [toInput, setToInput] = useState<number>(1000);
    const [productRating, setProductRating] = useState<number >(0);
    const [storeRating, setStoreRating] = useState<number >(0);

    const productType = {

    }
    const PostsData = ["category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news"];
    const products = [
        {
            name:'T-shirt',
            price:200,
            product_rating:5,
            store_rating: 5
        },
        {
            name:'T-shirt',
            price:200,
            product_rating:5,
            store_rating: 5
        },
        {
            name:'T-shirt',
            price:200,
            product_rating:5,
            store_rating: 5
        },
        {
            name:'T-shirt',
            price:200,
            product_rating:5,
            store_rating: 5
        },
        {
            name:'T-shirt',
            price:200,
            product_rating:5,
            store_rating: 5
        },
        {
            name:'T-shirt',
            price:200,
            product_rating:5,
            store_rating: 5
        },
        {
            name:'T-shirt',
            price:200,
            product_rating:5,
            store_rating: 5
        },
        {
            name:'T-shirt',
            price:200,
            product_rating:5,
            store_rating: 5
        },
    ]
    

    const handleFilter = (from:number,to:number,prodRate:number,storeRate:number)=>{
        setFromInput(from);
        setToInput(to);
        setProductRating(prodRate);
        setStoreRating(storeRate);

    }

    const filterProducts = ()=>{
        return products.filter((product)=>
        product.price >= fromInput && 
        product.price <= toInput &&
        product.product_rating >= productRating &&
        product.store_rating >= storeRating)
    }
      
    let matrix_length = 3;
    const setProductsInMatrix = (productsArray:any)=>{
        var matrix = [];
        for(var i=0; i<Math.ceil(productsArray.length/3); i++) {
            matrix[i] = new Array(matrix_length);
        }
        for(i=0; i<matrix.length; i++) {
            for(var j=0; j<matrix[i].length; j++){
                matrix[i][j] = productsArray[(matrix[i].length)*i+j];
            }
        }
        return matrix;
    }
	return (
		<div className="SearchPageDiv">
            <SearchCategory
                searchProduct = {searchProduct}
                categories={PostsData}
            />

            <div className="mainArea">
                <div className="filterArea">
                   <FilterMenu
                   handleFilter = {handleFilter}
                   />
                </div>
                <div className="productCards">
                    {setProductsInMatrix(filterProducts()).map((row,_)=>{
                        return(
                            <div className="cardsRow">
                                {row.map((cell,_)=>{
                                    return (
                                        
                                        <ProductSearch
                                            key={products.indexOf(cell)}
                                            content={cell!==undefined?cell.name:""}
                                        >
                                        </ProductSearch>
                                    )
                                })}
                            </div>
                        ) 
                        
                    })}
                </div>
            </div>
		</div>
	);
};
export default SearchPage;
