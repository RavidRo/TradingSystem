import React, { useState, FC} from 'react';
import StarBorderIcon from '@material-ui/icons/StarBorder';
import '../styles/FilterMenu.scss';

type FilterMenuProps = {
    handleFilter: (from:number,to:number)=>void
};

const FilterMenu: FC<FilterMenuProps> = ({handleFilter}) => {
 
    const [fromInput, setFromInput] = useState<string>("");
    const [toInput, setToInput] = useState<string>("");

    const handleApply = ()=>{
        handleFilter(parseInt(fromInput),parseInt(toInput))
    }
      
	return (
		<div className="filterMenu">
            <h3>Price</h3>
            <div className="price">
            <input className="fromPriceInput" onChange={(e)=>setFromInput(e.target.value)} value={fromInput}/>
            <h3>to</h3>
            <input className="toPriceInput" onChange={(e)=>setToInput(e.target.value)} value={toInput}/>
            </div>
            <br/>
            <button className="applyBtn" onClick={()=>handleApply()}>Apply</button>
        </div>
	);
};
export default FilterMenu;
