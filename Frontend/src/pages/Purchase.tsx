import { Button, TextField } from '@material-ui/core';
import React, { FC,useState,useEffect} from 'react';
import '../styles/Purchase.scss';
import Timer from '../components/Timer';
import useAPI from '../hooks/useAPI';
import getPropsCookie from '../pages/App';

type PurchaseProps = {
    location: any,

};

const Purchase: FC<PurchaseProps> = ({location}) => {
	const [totalAmount,setTotal] = useState<number>(location.state!==undefined?location.state.totalAmount:0);
    const [credit,setCredit] = useState<string>("");
    const [address,setAddress] = useState<string>("");
    // const [age,setAge] = useState<string>("");


    const purchaseObj = useAPI<number>('/send_payment',{},'POST');
    
    const handlePurchase = ()=>{
        purchaseObj.request({cookie: location.state.cookie,payment_details: {credit},address: address}).then(({data,error,errorMsg})=>{
            if(!error && data!==null){
                alert(data);
            }
            else{
                alert(errorMsg);
            }
            
        })
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
                        onChange={(e)=>setCredit(e.target.value)}
                    />
                    <TextField 
                        required 
                        id="standard-required" 
                        label="Address" 
                        defaultValue=""
                        style={{marginTop:'5%',width:'50%'}}
                        onChange={(e)=>setAddress(e.target.value)}
                    />
                    {/* <TextField 
                        required 
                        id="standard-required" 
                        label="Age" 
                        defaultValue=""
                        style={{marginTop:'5%',width:'50%'}}
                        onChange={(e)=>setAge(e.target.value)}
                    /> */}
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
