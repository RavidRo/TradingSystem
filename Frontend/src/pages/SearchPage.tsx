import React, { useState, FC, useEffect} from 'react';
import '../styles/SearchPage.scss';
import ProductSearch from '../components/ProductSearch';
import FilterMenu from '../components/FilterMenu';
import SearchCategory from '../components/SearchCategory';
import Keywards from '../components/Keywards';
import storesToProducts from '../components/storesProductsMap';
import storesProductsMap from '../components/storesProductsMap';
import useAPI from '../hooks/useAPI';

type SearchPageProps = {
    location: any,
    propsAddProduct:(product:Product)=>void,
};
type Product = {
    id:string,
    name:string,
    price: number,
    quantity:number
}

const SearchPage: FC<SearchPageProps> = ({location,propsAddProduct}) => {
    const [searchProduct, setSearchProduct] = useState<string>(location.state.product);
    const [category, setCategory] = useState<string>("");

    const [fromInput, setFromInput] = useState<number>(0);
    const [toInput, setToInput] = useState<number>(1000);
    const [productRating, setProductRating] = useState<number >(0);
    const [storeRating, setStoreRating] = useState<number >(0);

    const PostsData = ["category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news"];
    
    let products:Product[] = [];
    // TODO: get from server all products with 'searchProduct' name
    for(var i=0;i<Object.keys(storesToProducts).length;i++){
        for(var prod=0; prod<Object.values(storesToProducts)[i].length; prod++){
            products.push(Object.values(storesToProducts)[i][prod]);
        }
    }
    const getProductFromServer = ()=>{
        // let obj = useAPI("/getProduct",{productName:searchProduct,category:category,from:fromInput,to:toInput});
        // return obj.data;
    }

    const [productsToPresent,setProducts] = useState<Product[]>(products);
//     const [productsToPresent,setProducts] = useState<Product[]>(getProductFromServer());

    const handleFilter = (from:number,to:number,prodRate:number,storeRate:number)=>{
        setFromInput(from);
        setToInput(to);
        setProductRating(prodRate);
        setStoreRating(storeRate);
        // setProducts(getProductFromServer())

    }

    const filterProducts = ()=>{
        // TODO: send request to the server for filtering products
        return productsToPresent.filter((product)=>
        product.price >= fromInput && 
        product.price <= toInput )
        // setProducts(getProductFromServer())
        // return getProductFromServer()
    }
    const handleSearch = (toSearch:string,categoryName:string)=>{
        setSearchProduct(toSearch);
        setCategory(categoryName);
        // TODO: send request to server with toSearch and 
        // properties: category, prices, ratings
        // TODO: get products from server
        // setProducts(response)

        //  setProducts(getProductFromServer())
        
        let str = "product: "+toSearch+", category: "+categoryName+
        ", from: "+fromInput+", to: "+toInput;
        alert(str);
    }
    const clickAddProduct = (key:number)=>{
        propsAddProduct(products[key]);
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
    const findBagByProductID = (id:string)=>{
        for(var i=0; i<Object.keys(storesProductsMap).length;i++){
            let productsArray = (Object.values(storesProductsMap)[i]);
            for(var j=0; j<productsArray.length;j++){
                if(productsArray[j].id===id){
                    // return store name
                    return Object.keys(storesProductsMap)[i];
                }
            }
        }
        return "";
    }
	return (
		<div className="SearchPageDiv">
            <SearchCategory
                searchProduct = {searchProduct}
                categories={PostsData}
                handleSearch={handleSearch}
            />
            <Keywards></Keywards>
            
            <div className="mainArea">
                <div className="filterArea">
                   <FilterMenu
                   handleFilter = {handleFilter}
                   />
                </div>
                <div className="productCards">
                    {setProductsInMatrix(filterProducts()).map((row,i)=>{
                        return(
                            <div className="cardsRow">
                                {row.map((cell,j)=>{
                                    return (
                                        
                                        <ProductSearch
                                            key={i*matrix_length+j}
                                            id={cell!==undefined?cell.id:-1}
                                            storeName={cell!==undefined?findBagByProductID(cell.id):""}
                                            content={cell!==undefined?cell.name:""}
                                            price={cell!==undefined?cell.price:0}
                                            clickAddProduct={()=>clickAddProduct(products.indexOf(cell))}
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
