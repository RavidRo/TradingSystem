import React, { FC, useEffect, useState } from 'react';
import '../styles/SearchBar.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSearch } from '@fortawesome/free-solid-svg-icons';

type SearchBarProps = {};

const SearchBar: FC<SearchBarProps> = () => {
	
	return (
		<div className="SearchBarDiv">
			 <input 
                className="searchInput"
                key="random1"
                placeholder={"search product"}
                // onChange={(e) => setKeyword(e.target.value)}
                />
            <FontAwesomeIcon className="searchIcon" icon={faSearch} />

		</div>
	);
};
export default SearchBar;
