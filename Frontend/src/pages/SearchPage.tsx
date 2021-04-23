import { Button, Card, CardContent } from '@material-ui/core';
import React, { useState, FC} from 'react';
import '../styles/SearchPage.scss';

type SearchPageProps = {
    location: any,
};

const SearchPage: FC<SearchPageProps> = ({location}) => {
    const [searchProduct, setSearchProduct] = useState<string>(location.state.product);

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
                <button className="categoryBtn">
                    Category
                </button>
            </div>

            {matrix.map((row,row_i)=>{
                return(
                    <div className="cardsRow">
                        {row.map((cell,cell_i)=>{
                            return (
                                <Card 
                                    className="prodCard"
                                    key={cell_i}>
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
