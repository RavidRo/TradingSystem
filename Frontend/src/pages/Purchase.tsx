import { Button, TextField } from '@material-ui/core';
import React, { FC,useState,useEffect} from 'react';
import '../styles/Purchase.scss';
import Timer from '../components/Timer';
import useAPI from '../hooks/useAPI';

type PurchaseProps = {
    location: any,

};

const Purchase: FC<PurchaseProps> = ({location}) => {
	const [totalAmount,setTotal] = useState<number>(location.state!==undefined?location.state.totalAmount:0);
    const [ready,setReady] = useState<boolean>(false);

    const {request, data} = useAPI<number>('/purchase_cart');
    useEffect(()=>{
        request().then(()=>alert(data));
    },[ready]);
    
    const handlePurchase = ()=>{
        alert("Thank you for purchasing in Shopping World!");
    }

	return (
        <div className="purchaseDiv">
            <form  noValidate autoComplete="on">
                <div className="formDiv">
                    <TextField 
                        required 
                        id="standard-required" 
                        label="Credit Number" 
                        defaultValue=""
                        style={{width:'50%'}}
                    />
                    <TextField 
                        required 
                        id="standard-required" 
                        label="Address" 
                        defaultValue=""
                        style={{marginTop:'5%',width:'50%'}}
                    />
                    <TextField 
                        required 
                        id="standard-required" 
                        label="Age" 
                        defaultValue=""
                        style={{marginTop:'5%',width:'50%'}}
                    />
                </div>
                <h3 className="totalPurchase">
                    Total amount : {totalAmount}
                </h3>
                <Button 
                    className="purchaseBtn" 
                    style={{background:'#7FFF00',height:'50px',fontWeight:'bold',fontSize:'large',alignSelf:'center',marginLeft:'48%'}}
                    onClick={()=>handlePurchase()}
                    > 
                    Check
                </Button>
                <Timer/>
            </form>
        </div>
	);
};

export default Purchase;
