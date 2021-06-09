import React, { FC, useState, useEffect, useContext } from 'react';
import DateFnsUtils from "@date-io/date-fns"; // import
import { DatePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import { TextField } from '@material-ui/core';
import '../styles/Statistics.scss';
import useAPI from '../hooks/useAPI';
import {StatisticsData, StatisticsCount} from '../types';

type StatisticsProps = {
  statistics: StatisticsData | undefined
};

const Statistics: FC<StatisticsProps> = ({statistics}) => {
    const [fromDate, setFromDate] = useState<string>("");
    const [toDate, setToDate] = useState<string>("");
    const [statisticsMy, setStatistics] = useState<{ [date: string]: StatisticsCount }>();
    const statisticsObj = useAPI<StatisticsData>('/get_statistics', {}, 'GET');

    useEffect(()=>{
      if(statistics !== undefined){
        setStatistics(statistics.statistics_per_day);
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
        setFromDate(date);
        var dateObject = new Date(date);
        if(toDate !== ""){
          statisticsObj.request().then(({ data, error }) => {
            if (!error && data !== null) {
                setStatistics(data.data.statistics_per_day);
            }
          })
        }
    }

    const pickedTo = (e:any)=>{
        let date = e.target.value
        setToDate(date);
        var dateObject = new Date(date);

        if(fromDate !== ""){
          statisticsObj.request().then(({ data, error }) => {
            if (!error && data !== null) {
                setStatistics(data.data.statistics_per_day);
            }
          })
        }
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
                <ul>
                  {statisticsMy!==undefined ? Object.keys(statisticsMy).map((date)=>{
                    console.log(date);
                    console.log(toDate);
                    console.log(fromDate);
                    let small = fromDate.valueOf();
                    let big = toDate.valueOf();
                    let between = date.valueOf();

                    if(small <= between && between <= big){
                      let day_json = statisticsMy[date];
                      return (
                        <div>
                          <p>{date}</p>
                          {Object.keys(day_json).map((type, index)=>{
                            return (
                              <li key={index}>
                                {type} : {Object.values(day_json)[index]}
                              </li>
                            )
                          })}
                        </div>
                      )
                    }
                    
                  }):"No data"}
                </ul>
            </form>
        </div>

	);
};

export default Statistics;
