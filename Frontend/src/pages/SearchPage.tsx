import { Button, Card, CardContent, Typography } from '@material-ui/core';
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

            {matrix.map((row)=>{
                return(
                    <div className="cardsRow">
                        {row.map((cell)=>{
                            return (
                                <Card 
                                    className="prodCard"
                                    key={cell}>
                                    <CardContent>
                                        <Typography variant="body2" color="textSecondary" component="p">
                                            {cell}
                                        </Typography>
                                    </CardContent>
                                        <Button size="small" color="primary">
                                        Learn More
                                        </Button>
                                </Card>
                            )
                        })}
                    </div>
                ) 
                
            })}
            {/* <div className="app-card-list" id="app-card-list">
                <Grid container spacing={3} >
                    {PostsData.map(key => {
                        return (
                            <Grid container item xs={12} spacing={3}>
                                <Card >
                                    <CardContent>
                                        <Typography variant="body2" color="textSecondary" component="p">
                                            Lizards are a widespread group of squamate reptiles, with over 6,000 species, ranging
                                        </Typography>
                                    </CardContent>
                                        <Button size="small" color="primary">
                                        Learn More
                                        </Button>
                                </Card>
                            </Grid>
                        )}
                    )
                    }
                </Grid>
            </div> */}

		</div>
	);
};
export default SearchPage;
