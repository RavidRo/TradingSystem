import { Button, Card, CardContent } from '@material-ui/core';
import React, { useState, FC} from 'react';
import '../styles/SearchPage.scss';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCaretDown } from '@fortawesome/free-solid-svg-icons';


type SearchPageProps = {
    location: any,
};

const SearchPage: FC<SearchPageProps> = ({location}) => {
    const [searchProduct, setSearchProduct] = useState<string>(location.state.product);
    const [menuOpen, setMenuOpen] = useState<boolean>(false);
    const [categoryName, setCategoryName] = useState<string>("Category");

    const friendOptions = [
        'one', 'two', 'three'
      ]
    const PostsData = ["category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news","comedy",
                        "category","news"];
    var matrix = [];
    for(var i=0; i<Math.ceil(PostsData.length/3); i++) {
        matrix[i] = new Array(3);
    }
    for(i=0; i<matrix.length; i++) {
        for(var j=0; j<matrix[i].length; j++){
            matrix[i][j] = PostsData[(matrix[i].length)*i+j];
        }
        
    }

      
	return (
		<div className="SearchPageDiv">
            <div className="searchInputBtn">
                <input 
                    className="searchInput"
                    key="random1"
                    placeholder={"search product"}
                    value={searchProduct}
                    onChange={(e) => setSearchProduct(e.target.value)}
                />
                <div className="categoryDiv" onClick={()=>setMenuOpen(!menuOpen)}>
                    <button className="categoryBtn">
                        {categoryName}
                    <FontAwesomeIcon className="arrowIcon" icon={faCaretDown} />
                    </button>
                    {menuOpen?
                        <ul className="categoryList">
                            {PostsData.map((post)=>{
                                return (
                                    <button className="btn" onClick={()=>setCategoryName(post)}>
                                        {post}
                                    </button>
                                )
                            })}

                        </ul>
                    :null    
                }
                </div>
                
            </div>

            {matrix.map((row,row_i)=>{
                return(
                    <div className="cardsRow">
                        {row.map((cell,cell_i)=>{
                            return (
                                <Card 
                                    className="prodCard"
                                    key={(row_i*matrix.length)+cell_i}>
                                    <CardContent className="cardContent">
                                            {cell}
                                    </CardContent>
                                        <Button >
                                        Learn More
                                        </Button>
                                </Card>
                            )
                        })}
                    </div>
                ) 
                
            })}

		</div>
	);
};
export default SearchPage;
