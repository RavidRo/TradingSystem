import { Chip, Paper } from '@material-ui/core';
import React ,{FC, useState} from 'react';
import '../styles/Keywards.scss';

type Keywordsprops = {
  
};

const Keywards: FC<Keywordsprops> = () => {

    const [keyWords, setKeyWards] = useState<string[]>([]);
    const [currentKey, setCurrentKey] = useState<string>("");

    const handleDelete = (key:number)=>{
        setKeyWards(keyWords.filter((word)=>word!==keyWords[key]));
    }
    return (
		
		<div className="keywards">
            <input 
                className="keywordInput"
                onChange={(e) => setCurrentKey(e.target.value)}
            />

            <button className="keyBtn" onClick={()=>setKeyWards(old=>[...old,currentKey])}>Add</button>
                <div className="wardsDiv">
                    {keyWords.map((word) => {
                        let icon;

                        return (
                        <li key={keyWords.indexOf(word)}>
                            <Chip
                            label={word}
                            onDelete={()=>handleDelete(keyWords.indexOf(word))}
                            />
                        </li>
                        );
                    })}
                </div>
		</div>
	);
}

export default Keywards;
