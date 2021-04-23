import React, { useState, FC} from 'react';
import '../styles/SearchBar.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';
import { Link } from 'react-router-dom';
import {createBrowserHistory} from "history";


type SearchBarProps = {};

const SearchBar: FC<SearchBarProps> = () => {
	const [searchProd, setSearch] = useState<string>("");

	return (
		<div className="SearchBarDiv">
			 <input 
                className="searchInput"
                key="random1"
                placeholder={"search product"}
                value={searchProd}
                onChange={(e) => setSearch(e.target.value)}
                />
            <Link to={{
                pathname: '/searchPage',
                state: {
                    product: searchProd
                },
                }}>
                 <FontAwesomeIcon className="searchIcon" icon={faSearch} />
            </Link>

		</div>
	);
};
export default SearchBar;
