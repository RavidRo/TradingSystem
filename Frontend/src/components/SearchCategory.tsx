import React, { useState, FC} from 'react';
import '../styles/SearchBar.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons';
import '../styles/SearchCategory.scss';

type SearchCategoryProps = {
    searchProduct:string,
    categories:string[],
    handleSearch:(toSearch:string,categoryName:string)=>void
};

const SearchCategory: FC<SearchCategoryProps> = ({searchProduct, categories,handleSearch}) => {
    const [toSearch, setToSearch] = useState<string>(searchProduct);
    const [menuOpen, setMenuOpen] = useState<boolean>(false);
    const [categoryName, setCategoryName] = useState<string>("");


    
	return (
		<div className="searchInputBtn">
            <input 
                className="searchInput"
                key="random1"
                placeholder={"search product"}
                value={toSearch}
                onChange={(e) => setToSearch(e.target.value)}
            />
            <div className="categoryDiv" onClick={()=>setMenuOpen(!menuOpen)}>
                <button className="categoryBtn">
                    {categoryName!==""?categoryName:'Choose Category'}
                <FontAwesomeIcon className="arrowIcon" icon={faCaretDown} />
                </button>
                {menuOpen?
                    <ul className="categoryList">
                        {["All",...categories].map((category)=>{
                            return (
                                <button className="btn" onClick={()=>setCategoryName(category)}>
                                    {category}
                                </button>
                            )
                        })}

                    </ul>
                :null    
                }
            </div>
            <button className="searchBtn" onClick={()=>handleSearch(toSearch,categoryName)}>
                Search
            </button>
            
        </div>
	);
};
export default SearchCategory;
