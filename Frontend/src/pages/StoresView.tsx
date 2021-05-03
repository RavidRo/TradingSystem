import React ,{FC, useEffect, useState} from 'react';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import '../styles/StoresView.scss';
import ProductSearch from '../components/ProductSearch';
import storesToProducts from '../components/storesProductsMap';
import useAPI from '../hooks/useAPI';
import {Product,Store} from '../types';


type StoresViewProps = {
   propsAddProduct:(product:Product)=>void,
   location: any,

};

const StoresView: FC<StoresViewProps> = ({propsAddProduct,location}: StoresViewProps) => {

    const [presentProducts,setProducts] = useState<Product[]>([]);
    const [stores,setStores] = useState<Store[]>([]);

    const [store, setStore] = useState<string>(location.state!==undefined?location.state.storeID:"");
    const productsObj = useAPI<Product[]>('/get_products_by_store',{storeID:store});
    useEffect(()=>{
        productsObj.request().then(({data,error,errorMsg})=>{
            if(!error && data !==null){
                console.log(data.data);
                setProducts(data.data);
            }
            else{
                alert(errorMsg)
            }
            
        })
    },[store]);

    const storesObj = useAPI<Store[]>('/get_stores_details');
    useEffect(()=>{
        storesObj.request().then(({data,error,errorMsg})=>{
            console.log(data,error,errorMsg);
            if(!error && data !==null){
                console.log(data.data);
                setStores(data.data);
            }
            else{
                alert(errorMsg)
            }
            
        })
    },[]);

   const handleChange = (e:any)=>{
      setStore(e.target.value);
      let indexOfStore = Object.keys(storesToProducts).indexOf(e.target.value);
      setProducts(Object.values(storesToProducts)[indexOfStore]);
    //   TODO: request from server the products of this specific store
   }
   const matrix_length = 3;
   const setProductsInMatrix = ()=>{
      var matrix = [];
      for(var i=0; i<Math.ceil(presentProducts.length/3); i++) {
          matrix[i] = new Array(matrix_length);
      }
      for(i=0; i<matrix.length; i++) {
          for(var j=0; j<matrix[i].length; j++){
              matrix[i][j] = presentProducts[(matrix[i].length)*i+j];
          }
      }
      return matrix;
  }
    return (
		
		<div className="StoresDiv">
             <FormControl style={{'marginLeft':'5%','width':'100%','fontSize':'large','height':'94%'}}>
                <h3>Choose Store</h3>
                <Select
                value={store}
                style={{'fontSize': '2rem','width':'50%'}}
                onChange={(e)=>handleChange(e)}
                >
                   {stores.map((store)=>{
                      return(
                        <MenuItem value={store.name} key={Object.keys(storesToProducts).indexOf(store.name)}>{store.name}</MenuItem>
                      )
                   })}
                </Select>
                <div className="productCards">
                    {store!==""?
                    setProductsInMatrix().map((row,i)=>{
                        return(
                            <div className="cardsRow">
                                {row.map((cell,j)=>{
                                    return (
                                        
                                        <ProductSearch
                                            key={i*matrix_length+j}
                                            id={cell!==undefined?cell.id:-1}
                                            storeID={store}
                                            content={cell!==undefined?cell.name:""}
                                            price={cell!==undefined?cell.price:0}
                                            clickAddProduct={()=>propsAddProduct(cell)}
                                        >
                                        </ProductSearch>
                                    )
                                })}
                            </div>
                        ) 
                        
                    })
                  :
                  <div className="placeHolder">
                    </div>
                  }
                </div>
      </FormControl>
            
		</div>
	);
}

export default StoresView;
