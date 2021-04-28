import React, { useState, FC} from 'react';
import '../styles/SearchPage.scss';
import ProductSearch from '../components/ProductSearch';
import FilterMenu from '../components/FilterMenu';
import SearchCategory from '../components/SearchCategory';
import Keywards from '../components/Keywards';
import storesToProducts from '../components/storesProductsMap';

type SearchPageProps = {
    location: any,
    propsAddProduct:(product:Product)=>void,
};
type Product = {
    name:string,
    price: number,
    quantity:number
}

const SearchPage: FC<SearchPageProps> = ({location,propsAddProduct}) => {
    const [searchProduct, setSearchProduct] = useState<string>(location.state.product);
    
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
    for(var i=0;i<Object.keys(storesToProducts).length;i++){
        for(var prod=0; prod<Object.values(storesToProducts)[i].length; prod++){
            products.push(Object.values(storesToProducts)[i][prod]);
        }
    }
    const [productsToPresent,setProducts] = useState<Product[]>(products);

    const handleFilter = (from:number,to:number,prodRate:number,storeRate:number)=>{
        setFromInput(from);
        setToInput(to);
        setProductRating(prodRate);
        setStoreRating(storeRate);

    }

    const filterProducts = ()=>{
        // TODO: send request to the server for filtering products
        return productsToPresent.filter((product)=>
        product.price >= fromInput && 
        product.price <= toInput )
    }
    const handleSearch = (toSearch:string,categoryName:string)=>{
        setSearchProduct(toSearch);
        // TODO: send request to server with toSearch and 
        // properties: category, prices, ratings
        // TODO: get products from server
        // setProducts(response)
        
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
                    {setProductsInMatrix(filterProducts()).map((row,_)=>{
                        return(
                            <div className="cardsRow">
                                {row.map((cell,_)=>{
                                    return (
                                        
                                        <ProductSearch
                                            key={productsToPresent.indexOf(cell)}
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
