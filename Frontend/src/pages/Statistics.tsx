import React, { FC, useState, useEffect, useContext } from 'react';
// import DateFnsUtils from "@date-io/date-fns"; // import
// import { DatePicker, MuiPickersUtilsProvider } from "@material-ui/pickers";
import { TextField } from '@material-ui/core';
import '../styles/Statistics.scss';
import useAPI from '../hooks/useAPI';
import {StatisticsData, StatisticsCount} from '../types';
import Chart from "react-google-charts";


type StatisticsProps = {
  statistics: StatisticsData | undefined
};

const Statistics: FC<StatisticsProps> = ({statistics}) => {
    let fromDate = "2021-06-07";
    let toDate = "2021-06-07";
    const statisticsObj = useAPI<StatisticsData>('/get_statistics', {}, 'GET');
    const [dataGraph, setDataGraph] = useState<any[]>([]);

    useEffect(()=>{
      if(statistics !== undefined){
      }
    }, [statistics]);


    const pickedFrom = (e:any)=>{
        let date = e.target.value;
        fromDate = date;
        statisticsObj.request().then(({ data, error }) => {
          if (!error && data !== null) {
              let dataGraphResult = setDataToChart(data.data.statistics_per_day, fromDate, toDate);
              setDataGraph(dataGraphResult);
              console.log(data.data.statistics_per_day);
              console.log(dataGraphResult);
          }
        })
    }

    const pickedTo = (e:any)=>{
        let date = e.target.value;
        toDate = date;
        statisticsObj.request().then(({ data, error }) => {
          if (!error && data !== null) {
              let dataGraphResult = setDataToChart(data.data.statistics_per_day, fromDate, toDate);
              setDataGraph(dataGraphResult);
              console.log(data.data.statistics_per_day);
              console.log(dataGraphResult);
          }
        })
    }

    // data={[
    //   ['Statistics', 'guests', 'passive members', 'users', 'managers', 'owners', 'super members'],
    //   ['2021-06-09', 1000, 400, 200, 0,0 , 0],
    //   ['2021-06-10', 1170, 460, 250,0, 0 , 0],
    //   ['2021-06-08', 660, 1120, 300, 0,0 , 0],
    //   ['2021-06-07', 1030, 540, 350,0, 0 , 0],
    // ]}

    const usersTypes = ['guest', 'passive_members', 'users', 'managers', 'owners', 'super_members'];
    const setDataToChart = (dataJson: { [date: string]: StatisticsCount }, fromDate: string, toDate: string)=>{
        return Object.keys(dataJson).map((date)=>{
          let small = fromDate.valueOf();
          let big = toDate.valueOf();
          let between = date.valueOf();
          console.log(small <= between);
          console.log(between <= big);
          if(small <= between && between <= big){
            let specificDateArr = [];
            specificDateArr.push(date); //first arg - date
            let statisticsJson = dataJson[date];
            for(var i=0; i<usersTypes.length; i++){
              let userType = usersTypes[i];
              if(statisticsJson.hasOwnProperty(userType)){ // user type is in this date, add it's value
                let index = Object.keys(statisticsJson).indexOf(userType);
                let userTypeValue = Object.values(statisticsJson)[index];
                specificDateArr.push(userTypeValue);
              }
              else{//no user type in this date, add 0
                specificDateArr.push(0);
              }
            }
            return specificDateArr;
          }
          return [];
      })
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
                <Chart
                    width={'2000px'}
                    height={'600px'}
                    style={{marginTop: '8%', marginLeft: '5%'}}
                    chartType="Bar"
                    loader={<div>Loading Chart</div>}
                    data={[
                      ['Statistics', 'guests', 'passive members', 'users', 'managers', 'owners', 'super members'],
                      ...dataGraph
                    ]}
                    options={{
                      // Material design options
                      chart: {
                        title: 'Website Statistics',
                        subtitle: 'guests, passive members, users, managers, owners, super members',
                      },
                    }}
                    // For tests
                    rootProps={{ 'data-testid': '2' }}
                  />
            </form>
        </div>

	);
};

export default Statistics;
