import React, { useState, FC} from 'react';
import '../styles/SearchBar.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons';
import '../styles/SearchCategory.scss';

type SearchCategoryProps = {
    searchProduct:string,
    categories:string[],
};

const SearchCategory: FC<SearchCategoryProps> = ({searchProduct, categories}) => {
    const [toSearch, setToSearch] = useState<string>(searchProduct);
    const [menuOpen, setMenuOpen] = useState<boolean>(false);
    const [categoryName, setCategoryName] = useState<string>("Category");


    
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
                    {categoryName}
                <FontAwesomeIcon className="arrowIcon" icon={faCaretDown} />
                </button>
                {menuOpen?
                    <ul className="categoryList">
                        {categories.map((category)=>{
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
            
        </div>
	);
};
export default SearchCategory;
