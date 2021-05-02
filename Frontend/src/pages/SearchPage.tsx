import React, { useState, FC, useEffect, useRef} from 'react';
import '../styles/SearchPage.scss';
import ProductSearch from '../components/ProductSearch';
import FilterMenu from '../components/FilterMenu';
import SearchCategory from '../components/SearchCategory';
import Keywards from '../components/Keywards';
import useAPI from '../hooks/useAPI';
import {Product,ProductQuantity,Store,StoreToSearchedProducts} from '../types';

type SearchPageProps = {
    location: any,
    propsAddProduct:(product:Product)=>void,
};


const SearchPage: FC<SearchPageProps> = ({location,propsAddProduct}) => {
    const [searchProduct, setSearchProduct] = useState<string>(location.state.product);
    const [category, setCategory] = useState<string>("");
    const [keyWords, setKeyWards] = useState<string[]>([]);

    const categories = ['news','clothes','food','shows','makeUp','photos'];
    const [fromInput, setFromInput] = useState<number>(0);
    const [toInput, setToInput] = useState<number>(1000);
    const [productRating, setProductRating] = useState<number >(0);
    const [storeRating, setStoreRating] = useState<number >(0);

    const storeToSearchedProducts = useRef<StoreToSearchedProducts>([]);
    const [productsToPresent,setProducts] = useState<ProductQuantity[]>([]);
    const [stores,setStores] = useState<Store[]>([]);

   
    const storesToProductsObj = useAPI<StoreToSearchedProducts>('/search_products');
    useEffect(()=>{
        console.log(keyWords);
        storesToProductsObj.request(
            {product_name:searchProduct,category:category,min_price:fromInput,max_price:toInput,kwargs:keyWords})
            .then(({data,error,errorMsg})=>{

            if(!error && data!==null){
                storeToSearchedProducts.current = data.data;
                let productQuantitiesArr:ProductQuantity[] = [];
                for(var i=0;i<storeToSearchedProducts.current.length;i++){
                    let storeProductQuanMap = storeToSearchedProducts.current[i];
                    let productQuantities = storeProductQuanMap.productQuantities;
                    for(var j=0;j<productQuantities.length;j++){
                        setProducts(old=>[...old,{id:productQuantities[j][0].id,
                            name:productQuantities[j][0].name,
                            category:productQuantities[j][0].category,
                            price:productQuantities[j][0].price,
                            keywords:productQuantities[j][0].keywords,
                            quantity:productQuantities[j][1]}])
                    }
                    
                }
            }
            else{
                alert(errorMsg)
            }
        })
    },[searchProduct,category,fromInput,toInput,keyWords]);


    const handleFilter = (from:number,to:number,prodRate:number,storeRate:number)=>{
        setFromInput(from);
        setToInput(to);
        setProductRating(prodRate);
        setStoreRating(storeRate);
        // all the set methods make useEffect to re-render and ask for server
        // to send new products

    }

    const handleSearch = (toSearch:string,categoryName:string)=>{
        setSearchProduct(toSearch);
        setCategory(categoryName);
        // all the set methods make useEffect to re-render and ask for server
        // to send new products
    }
    const clickAddProduct = (key:number)=>{
        propsAddProduct(productsToPresent[key]);
    }
    const updateKeyWords = (keyWords:string[])=>{
        setKeyWards(keyWords);
        // all the set methods make useEffect to re-render and ask for server
        // to send new products
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

        for(var i=0;i<storeToSearchedProducts.current.length;i++){
            let storeProductQuanMap = storeToSearchedProducts.current[i];
            let productQuantities = storeProductQuanMap.productQuantities;
            for(var j=0;j<productQuantities.length;j++){
                if(productQuantities[j][0].id===id){
                    return storeProductQuanMap.storeID;
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
                                            quantity={cell!==undefined?cell.quantity:0}
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
