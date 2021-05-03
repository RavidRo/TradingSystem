import React, { useState, FC, useEffect, useRef} from 'react';
import '../styles/SearchPage.scss';
import ProductSearch from '../components/ProductSearch';
import FilterMenu from '../components/FilterMenu';
import SearchCategory from '../components/SearchCategory';
import Keywards from '../components/Keywards';
import storesToProducts from '../components/storesProductsMap';
import storesProductsMap from '../components/storesProductsMap';
import useAPI from '../hooks/useAPI';
import {Product} from '../types';

type SearchPageProps = {
    location: any,
    propsAddProduct:(product:Product)=>void,
};
type storesToProductsMapType = {
    [key:string]:Product[]
}

const SearchPage: FC<SearchPageProps> = ({location,propsAddProduct}) => {
    const [searchProduct, setSearchProduct] = useState<string>(location.state.product);
    const [category, setCategory] = useState<string>("");
    const [keyWords, setKeyWards] = useState<string[]>([]);

    const categories = ['news','clothes','food','shows','makeUp','photos'];
    const [fromInput, setFromInput] = useState<number>(0);
    const [toInput, setToInput] = useState<number>(1000);
    const [productRating, setProductRating] = useState<number >(0);
    const [storeRating, setStoreRating] = useState<number >(0);

    const storesToProductsMap = useRef<storesToProductsMapType>({});
    const [productsToPresent,setProducts] = useState<Product[]>([]);

    // TODO: find out exactly what is returning from server
    // and parse it correctly
    const productObj = useAPI<Product[]>('/search_products',{product_name:searchProduct,category:category,min_price:fromInput,max_price:toInput,kwargs:keyWords});
    useEffect(()=>{
        productObj.request().then(({data,error,errorMsg})=>{
            if(!error && data!==null){
                // setProducts(productObj.data);
            }
            else{
                alert(errorMsg)
            }
        })
    },[searchProduct,category,fromInput,toInput]);
    
    
    const storesProductsObj = useAPI<storesToProductsMapType>('/search_product',{searchProduct:searchProduct,category:category,from:fromInput,to:toInput});
    useEffect(()=>{
        storesProductsObj.request().then(({data,error,errorMsg})=>{
            if(!error && data!==null){
                // storesTo
                storesToProductsMap.current = data.data;
            }
            else{
                alert(errorMsg)
            }
        })
    },[searchProduct,category,fromInput,toInput]);

    // let products:Product[] = [];
    // // TODO: get from server all products with 'searchProduct' name
    // for(var i=0;i<Object.keys(storesToProducts).length;i++){
    //     for(var prod=0; prod<Object.values(storesToProducts)[i].length; prod++){
    //         products.push(Object.values(storesToProducts)[i][prod]);
    //     }
    // }


    const handleFilter = (from:number,to:number,prodRate:number,storeRate:number)=>{
        setFromInput(from);
        setToInput(to);
        setProductRating(prodRate);
        setStoreRating(storeRate);

    }

    const handleSearch = (toSearch:string,categoryName:string)=>{
        setSearchProduct(toSearch);
        setCategory(categoryName);
    }
    const clickAddProduct = (key:number)=>{
        propsAddProduct(productsToPresent[key]);
    }
    const updateKeyWords = (keyWords:string[])=>{
        setKeyWards(keyWords);
    }
    let matrix_length = 3;
    const setProductsInMatrix = ()=>{
        var matrix = [];
        for(var i=0; i<Math.ceil(productsToPresent.length/3); i++) {
            matrix[i] = new Array(matrix_length);
        }
        for(i=0; i<matrix.length; i++) {
            for(var j=0; j<matrix[i].length; j++){
                matrix[i][j] = productsToPresent[(matrix[i].length)*i+j];
            }
        }
        return matrix;
    }
    const findBagIDByProductID = (id:string)=>{
        for(var i=0; i<Object.keys(storesToProductsMap.current).length;i++){
            let productsArray = (Object.values(storesToProductsMap.current)[i]);
            for(var j=0; j<productsArray.length;j++){
                if(productsArray[j].id===id){
                    // return store name
                    return Object.keys(storesToProductsMap)[i];
                }
            }
        }
        return "";
    }
	return (
		<div className="SearchPageDiv">
            <SearchCategory
                searchProduct = {searchProduct}
                categories={categories}
                handleSearch={handleSearch}
            />
            <Keywards updateKeyWords={updateKeyWords}></Keywards>
            
            <div className="mainArea">
                <div className="filterArea">
                   <FilterMenu
                   handleFilter = {handleFilter}
                   />
                </div>
                <div className="productCards">
                    {setProductsInMatrix().map((row,i)=>{
                        return(
                            <div className="cardsRow">
                                {row.map((cell,j)=>{
                                    return (
                                        
                                        <ProductSearch
                                            key={i*matrix_length+j}
                                            id={cell!==undefined?cell.id:-1}
                                            storeID={cell!==undefined?findBagIDByProductID(cell.id):""}
                                            content={cell!==undefined?cell.name:""}
                                            price={cell!==undefined?cell.price:0}
                                            clickAddProduct={()=>clickAddProduct(productsToPresent.indexOf(cell))}
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
