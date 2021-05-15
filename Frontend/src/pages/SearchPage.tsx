import React, { useState, FC, useEffect, useRef} from 'react';
import '../styles/SearchPage.scss';
import ProductSearch from '../components/ProductSearch';
import FilterMenu from '../components/FilterMenu';
import SearchCategory from '../components/SearchCategory';
import Keywards from '../components/Keywards';
import useAPI from '../hooks/useAPI';
import {Product,ProductQuantity,Store,StoreToSearchedProducts} from '../types';
import Swal from 'sweetalert2';

type SearchPageProps = {
    location: any,
    propsAddProduct:(product:Product,storeID:string)=>Promise<boolean>,
};


const SearchPage: FC<SearchPageProps> = ({location,propsAddProduct}) => {
    const [searchProduct, setSearchProduct] = useState<string>(location.state.product);
    const [category, setCategory] = useState<string>("");
    const [keyWords, setKeyWards] = useState<string[]>([]);

    const [fromInput, setFromInput] = useState<number>(0);
    const [toInput, setToInput] = useState<number>(1000);
    const [productRating, setProductRating] = useState<number >(0);
    const [storeRating, setStoreRating] = useState<number >(0);

    const storeToSearchedProducts = useRef<StoreToSearchedProducts>({});
    const [productsToPresent,setProducts] = useState<ProductQuantity[]>([]);
    const [stores,setStores] = useState<Store[]>([]);
    const firstRender = useRef<boolean>(true);
   
    const allCategories = useRef<string[]>([]);
    const storesToProductsObj = useAPI<StoreToSearchedProducts>('/search_products');
    useEffect(()=>{
        
        storesToProductsObj.request(
            {product_name:searchProduct,category:category,min_price:fromInput,max_price:toInput,kwargs:keyWords})
            .then(({data,error,errorMsg})=>{

            if(!error && data!==null){
                storeToSearchedProducts.current = data.data;
                let productsToQuantities:ProductQuantity[] = [];
                for(var i=0;i<Object.keys(storeToSearchedProducts.current).length;i++){
                    let productQuantities = Object.values(storeToSearchedProducts.current)[i];
                    for(var j=0;j<productQuantities.length;j++){
                        productsToQuantities.push(
                            {id:productQuantities[j][0].id,
                                name:productQuantities[j][0].name,
                                category:productQuantities[j][0].category,
                                price:productQuantities[j][0].price,
                                keywords:productQuantities[j][0].keywords,
                                quantity:productQuantities[j][1]
                            }
                        )
                        if(!allCategories.current.includes(productQuantities[j][0].category)){
                            allCategories.current.push(productQuantities[j][0].category);
                        }
                    }
                    if(firstRender.current===false){
                        setProducts(productsToQuantities);
                    }
                    else{
                        setProducts(old=>[...old,...productsToQuantities]);
                    }
                    
                    firstRender.current = false;
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
        setCategory(categoryName==="All"?"":categoryName);
        // all the set methods make useEffect to re-render and ask for server
        // to send new products
    }
    const clickAddProduct = (key:number,storeID:string)=>{
        let response = propsAddProduct(productsToPresent[key],storeID);
        response.then((result)=>{
            if(result===true){
                Swal.fire({
                    icon: 'success',
                    title: 'Congratulations!',
                    text: 'The item added to cart successfully',
                  })
            }
        })
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
        for(var i=0;i<Object.keys(storeToSearchedProducts.current).length;i++){
            let productQuantities = Object.values(storeToSearchedProducts.current)[i];
            for(var j=0;j<productQuantities.length;j++){
                if(productQuantities[j][0].id===id){
                    return Object.keys(storeToSearchedProducts.current)[i];
                }
            }
        }
        return "";
    }
    const handleAddToCart = (storeID:string,key:number)=>{
        if(storeID!==""){//dummy product
            clickAddProduct(key,storeID);
        }
    }
   
	return (
		<div className="SearchPageDiv">
            <SearchCategory
                searchProduct = {searchProduct}
                categories={allCategories.current}
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
                                            storeID={cell!==undefined?findBagIDByProductID(cell.id):""}
                                            content={cell!==undefined?cell.name:""}
                                            price={cell!==undefined?cell.price:0}
                                            quantity={cell!==undefined?cell.quantity:0}
                                            category={cell!==undefined?cell.category:""}
                                            keywords={cell!==undefined?cell.keywords:""}
                                            clickAddProduct={()=>handleAddToCart(cell!==undefined?findBagIDByProductID(cell.id):"",productsToPresent.indexOf(cell))}
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
