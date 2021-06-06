import React, { FC, useState, useEffect, useContext } from 'react';
import DateFnsUtils from "@date-io/date-fns"; // import
import { DatePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import { TextField } from '@material-ui/core';
import '../styles/Statistics.scss';


type StatisticsProps = {
};

const Statistics: FC<StatisticsProps> = ({
}) => {
    const [fromDate, setFromDate] = useState<string>("");
    const [toDate, setToDate] = useState<string>("");

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
        <form noValidate>
            <TextField
                className="fromDate"
                id="date"
                label="From"
                type="date"
                defaultValue="2017-05-24"
                InputLabelProps={{
                shrink: true,
                }}
                onChange={(e)=>pickedFrom(e)}
                style={{width: 200, marginRight: 50}}
            />
            <TextField
                className="toDate"
                id="date"
                label="To"
                type="date"
                defaultValue="2017-05-24"
                InputLabelProps={{
                shrink: true,
                }}
                onChange={(e)=>pickedTo(e)}
                style={{width: 200}}
            />
        </form>

	);
};

export default Statistics;
