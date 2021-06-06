import React, { FC, useState, useEffect, useContext } from 'react';
import DateFnsUtils from "@date-io/date-fns"; // import
import { DatePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import { TextField } from '@material-ui/core';
import '../styles/Statistics.scss';


type StatisticsProps = {
};

const Statistics: FC<StatisticsProps> = ({}) => {
    const [fromDate, setFromDate] = useState<string>("");
    const [toDate, setToDate] = useState<string>("");

    const styles = {
        inputRoot: {
          fontSize: 30
        },
        labelRoot: {
          fontSize: 30,
          color: "red",
          "&$labelFocused": {
            color: "purple"
          }
        },
        labelFocused: {}
      };

    const pickedFrom = (e:any)=>{
        let date = e.target.value
        console.log(date);
        setFromDate(date);
        var dateObject = new Date(date);
        console.log(dateObject)

    }
    const pickedTo = (e:any)=>{
        let date = e.target.value
        console.log(date);
        setToDate(date);
        var dateObject = new Date(date);
        console.log(dateObject)

    }

	return (
        <div className="statistics">
            <form noValidate>
                <TextField
                    className="fromDate"
                    id="date"
                    label="From"
                    type="date"
                    defaultValue="2017-05-24"
                    onChange={(e)=>pickedFrom(e)}
                    style={{width: 200, marginRight: 50, marginTop: 30}}
                    inputProps={{style: {fontSize: 20, marginTop: 20}}} 
                    InputLabelProps={{style: {fontSize: 30}}}
                   
                />
                <TextField
                    className="toDate"
                    id="date"
                    label="To"
                    type="date"
                    defaultValue="2017-05-24"
                    onChange={(e)=>pickedTo(e)}
                    style={{width: 200,  marginTop: 30}}
                    inputProps={{style: {fontSize: 20, marginTop: 20}}} 
                    InputLabelProps={{style: {fontSize: 30}}}
                />
            </form>
        </div>

	);
};

export default Statistics;
