import { Chip } from '@material-ui/core';
import React ,{FC, useState, useRef} from 'react';
import '../styles/Keywards.scss';

type Keywordsprops = {
    updateKeyWords:(keywords:string[])=>void,
};

const Keywards: FC<Keywordsprops> = ({updateKeyWords}) => {

    const keyWords = useRef<string[]>([]);
    const [currentKey, setCurrentKey] = useState<string>("");

    const handleDelete = (key:number)=>{
        keyWords.current = keyWords.current.filter((word)=>word!==keyWords.current[key]);
        updateKeyWords(keyWords.current);
    }
    const handleAddWord = ()=>{
        if(currentKey === ""){
            alert("you can not add empty keyword");
        }
        else{
            keyWords.current = [...keyWords.current, currentKey];
            updateKeyWords(keyWords.current);
        }
    }
    return (
		
		<div className="keywards">
            <p className="wordsP" style={{'marginTop':'2%'}}>
                Search by Key Words:
            </p>
            <input 
                className="keywordInput"
                onChange={(e) => setCurrentKey(e.target.value)}
            />

            <button className="keyBtn" onClick={()=>handleAddWord()}>Add</button>
                <div className="wardsDiv">
                    {keyWords.current.map((word) => {
                        return (
                        <li key={keyWords.current.indexOf(word)}>
                            <Chip
                            label={word}
                            onDelete={()=>handleDelete(keyWords.current.indexOf(word))}
                            />
                        </li>
                        );
                    })}
                </div>
		</div>
	);
}

export default Keywards;
