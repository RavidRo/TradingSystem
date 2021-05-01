import { Chip } from '@material-ui/core';
import React ,{FC, useState} from 'react';
import '../styles/Keywards.scss';

type Keywordsprops = {
    updateKeyWords:(keywords:string[])=>void,
};

const Keywards: FC<Keywordsprops> = ({updateKeyWords}) => {

    const [keyWords, setKeyWards] = useState<string[]>([]);
    const [currentKey, setCurrentKey] = useState<string>("");

    const handleDelete = (key:number)=>{
        setKeyWards(keyWords.filter((word)=>word!==keyWords[key]));
        updateKeyWords(keyWords);
    }
    const handleAddWord = ()=>{
        setKeyWards(old=>[...old,currentKey]);
        updateKeyWords(keyWords);
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
                    {keyWords.map((word) => {
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
