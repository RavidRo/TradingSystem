import React, { FC, useState, useEffect, useContext } from 'react';
import DateFnsUtils from "@date-io/date-fns"; // import
import { DatePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import { TextField } from '@material-ui/core';
import '../styles/Statistics.scss';
import useAPI from '../hooks/useAPI';
import {StatisticsData} from '../types';

type StatisticsProps = {
  statistics: StatisticsData | undefined
};

const Statistics: FC<StatisticsProps> = ({statistics}) => {
    const [fromDate, setFromDate] = useState<string>("");
    const [toDate, setToDate] = useState<string>("");
    const [statisticsMy, setStatistics] = useState<StatisticsData>();
    const statisticsObj = useAPI<StatisticsData>('/get_statistics', {}, 'GET');

    useEffect(()=>{
      if(statistics !== undefined){
        setStatistics(statistics);
      }
    }, [statistics]);


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
                    defaultValue="2021-06-07"
                    onChange={(e)=>pickedFrom(e)}
                    style={{width: '10%', marginRight: '5%', marginTop: '5%', marginLeft: '35%'}}
                    inputProps={{style: {fontSize: 20, marginTop: 20}}} 
                    InputLabelProps={{style: {fontSize: 30}}}
                   
                />
                <TextField
                    className="toDate"
                    id="date"
                    label="To"
                    type="date"
                    defaultValue="2021-06-07"
                    onChange={(e)=>pickedTo(e)}
                    style={{width: '10%', marginTop: '5%'}}
                    inputProps={{style: {fontSize: 20, marginTop: 20}}} 
                    InputLabelProps={{style: {fontSize: 30}}}
                />

                {fromDate !== "" && toDate !== ""?
                statisticsObj.request({})
                .then(({ data, error }) => {
                  if (!error && data !== null) {
                      setStatistics(data.data);
                      console.log(data.data);
                }
              }):null}
            </form>
        </div>

	);
};

export default Statistics;
