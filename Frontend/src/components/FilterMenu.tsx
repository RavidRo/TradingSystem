import React, { useState, FC} from 'react';
import Rating from '@material-ui/lab/Rating';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import '../styles/FilterMenu.scss';

type FilterMenuProps = {
    handleFilter: (from:number,to:number,prodRate:number,storeRate:number)=>void
};

const FilterMenu: FC<FilterMenuProps> = ({handleFilter}) => {
 
    const [fromInput, setFromInput] = useState<string>("");
    const [toInput, setToInput] = useState<string>("");
    const [productRating, setProductRating] = useState<number | null>(null);
    const [storeRating, setStoreRating] = useState<number | null>(null);

    const handleApply = ()=>{
        handleFilter(parseInt(fromInput),parseInt(toInput),
        productRating!==null?productRating:0, storeRating!==null?storeRating:0)
    }
      
	return (
		<div className="filterMenu">
            <h3>Price</h3>
            <div className="price">
            <input className="fromPriceInput" onChange={(e)=>setFromInput(e.target.value)} value={fromInput}/>
            <h3>to</h3>
            <input className="toPriceInput" onChange={(e)=>setToInput(e.target.value)} value={toInput}/>
            </div>
            <h3>Avg Product Rating</h3>
            <div className="productRating">
                <Rating
                    name="productRate"
                    defaultValue={2}
                    precision={0.5}
                    emptyIcon={<StarBorderIcon fontSize="inherit" style={{'fill':'black'}}/>}
                    onChange={(event, newValue) => {
                        setProductRating(newValue);
                    }}
                />
                <p>{productRating}</p>
            </div>
            <h3>Avg Store Rating</h3>
            <div className="storeRating">
                <Rating
                    name="storeRate"
                    defaultValue={2}
                    precision={0.5}
                    emptyIcon={<StarBorderIcon fontSize="inherit" style={{'fill':'black'}}/>}
                    onChange={(event, newValue) => {
                        setStoreRating(newValue);
                    }}
                />
                <p>{storeRating}</p>
            </div>
            <br/>
            <button className="applyBtn" onClick={()=>handleApply()}>Apply</button>
        </div>
	);
};
export default FilterMenu;
