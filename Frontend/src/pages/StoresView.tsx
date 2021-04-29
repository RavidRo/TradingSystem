import React ,{FC, useState} from 'react';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import MenuItem from '@material-ui/core/MenuItem';
import '../styles/StoresView.scss';
import ProductSearch from '../components/ProductSearch';
import storesToProducts from '../components/storesProductsMap';

type StoresViewProps = {
   propsAddProduct:(product:Product)=>void,
   location: any,

};
type Product = {
    id:number,
   name:string,
   price: number,
   quantity: number,
}
const StoresView: FC<StoresViewProps> = ({propsAddProduct,location}: StoresViewProps) => {

    const [store, setStore] = useState<string>(location.state!==undefined?location.state.storeName:"");
   
    const [presentProducts,setProducts] = useState<Product[]>(
        location.state!==undefined?Object.values(storesToProducts)[
            Object.keys(storesToProducts).indexOf(location.state.storeName)
        ]
        :[]
    );

   const handleChange = (e:any)=>{
      setStore(e.target.value);
      let indexOfStore = Object.keys(storesToProducts).indexOf(e.target.value);
      setProducts(Object.values(storesToProducts)[indexOfStore]);
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
             <FormControl style={{'marginLeft':'20%','width':'50%','fontSize':'large'}}>
                <h3>Choose Store</h3>
                <Select
                value={store}
                style={{'fontSize': '2rem'}}
                onChange={(e)=>handleChange(e)}
                >
                   {Object.keys(storesToProducts).map((store)=>{
                      return(
                        <MenuItem value={store} key={Object.keys(storesToProducts).indexOf(store)}>{store}</MenuItem>
                      )
                   })}
                </Select>
                <div className="productCards">
                    {store!==""?
                    setProductsInMatrix().map((row,_)=>{
                        return(
                            <div className="cardsRow">
                                {row.map((cell,_)=>{
                                    return (
                                        
                                        <ProductSearch
                                            key={presentProducts.indexOf(cell)}
                                            id={cell!==undefined?cell.id:-1}
                                            storeName={store}
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
                  :null}
                </div>
      </FormControl>
            
		</div>
	);
}

export default StoresView;
