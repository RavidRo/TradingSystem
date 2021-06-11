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
    let today = new Date().toISOString().slice(0, 10);
    let fromDate = "2021-06-07";
    let toDate = today;
    const [from, setFrom] = useState<string>("2021-06-07");
    const [to, setTo] = useState<string>(today);

    const statisticsObj = useAPI<StatisticsData>('/get_statistics', {}, 'GET');
    const [dataGraph, setDataGraph] = useState<any[]>([]);
    const [dataPie, setDataPie] = useState<any[]>([]);
    const [data,setDate] = useState<{ [date: string]: StatisticsCount }>({})

    useEffect(()=>{
      console.log("in here !!!");
      statisticsObj.request().then(({ data, error }) => {
        if (!error && data !== null) {
            let dataGraphResult = setDataToChart(data.data.statistics_per_day, from, to);
            setDataGraph(dataGraphResult);
            let pieResult = setDataToPie(data.data.statistics_per_day);
            setDataPie(pieResult);
            setDate(data.data.statistics_per_day);
        }
      })
    }, [statistics]);


    const pickedFrom = (e:any)=>{
        let date = e.target.value;
        fromDate = date;
        setFrom(fromDate);
        statisticsObj.request().then(({ data, error }) => {
          if (!error && data !== null) {
              let dataGraphResult = setDataToChart(data.data.statistics_per_day, fromDate, toDate);
              setDataGraph(dataGraphResult);
              let pieResult = setDataToPie(data.data.statistics_per_day);
              setDataPie(pieResult);
              setDate(data.data.statistics_per_day);
          }
        })
    }

    const pickedTo = (e:any)=>{
        let date = e.target.value;
        toDate = date;
        setTo(toDate);
        statisticsObj.request().then(({ data, error }) => {
          if (!error && data !== null) {
              let dataGraphResult = setDataToChart(data.data.statistics_per_day, fromDate, toDate);
              setDataGraph(dataGraphResult);
              let pieResult = setDataToPie(data.data.statistics_per_day);
              setDataPie(pieResult);
              setDate(data.data.statistics_per_day);
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
    const setDataToPie = (dataJson: { [date: string]: StatisticsCount })=>{
      let usersJson:{ [type: string]: number } = {};
      Object.keys(dataJson).map((date)=>{
        let small = fromDate.valueOf();
        let big = toDate.valueOf();
        let between = date.valueOf();
        if(small <= between && between <= big){
          let statisticsJson:StatisticsCount = dataJson[date];
          for(var i=0; i<usersTypes.length; i++){
            let userType = usersTypes[i];
            if(statisticsJson.hasOwnProperty(userType)){ // user type is in this date, add it's value
              let index = Object.keys(statisticsJson).indexOf(userType);
              let userTypeValue = +Object.values(statisticsJson)[index];
              if (usersJson.hasOwnProperty(userType)){
                usersJson[userType] += userTypeValue;
              }
              else{
                usersJson[userType] = userTypeValue;
              }
            }
          }
        }

      })

      let finalArr = [];
      for(var i=0; i<Object.keys(usersJson).length; i++){
        let type = Object.keys(usersJson)[i];
        let value = Object.values(usersJson)[i];
        finalArr.push([type, value]);
      }
      return finalArr;
    }

	return (
        <div className="statistics">
            <form noValidate>
                <TextField
                    className="fromDate"
                    id="date"
                    label="From"
                    type="date"
                    defaultValue={from}
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
                    defaultValue={to}
                    onChange={(e)=>pickedTo(e)}
                    style={{width: '15%', marginTop: '5%'}}
                    inputProps={{style: {fontSize: 20, marginTop: 20}}} 
                    InputLabelProps={{style: {fontSize: 30}}}
                />
                <div className="charts">
                  <ul className="dataList">
                  {Object.keys(data).map((date)=>{
                    let small = from.valueOf();
                    let big = to.valueOf();
                    let between = date.valueOf();
                    if(small <= between && between <= big){

                      let index = Object.keys(data).indexOf(date);
                      let jsonStat = Object.values(data)[index];
                      return (
                        <li key={index} className="date">
                          <h2>{date}</h2>
                          {Object.keys(jsonStat).map((type)=>{
                            let typeIndex = Object.keys(jsonStat).indexOf(type);
                            return (
                              <h3>
                                {type}  :  {Object.values(jsonStat)[typeIndex]}
                              </h3>
                            )
                          })}
                        </li>
                      )
                    }
                  })}
                  </ul>
                  {dataPie.length === 0? null:
                    <Chart
                      width={'500px'}
                      height={'300px'}
                      chartType="PieChart"
                      loader={<div>Loading Chart</div>}
                      style={{marginTop: '4%', marginLeft: '3%'}}
                      data={[
                        ['Users', 'Amount'],
                        ...dataPie
                      ]}
                      options={{
                        title: 'Users from Total',
                      }}
                      rootProps={{ 'data-testid': '1' }}
                    />
                  }
                    {dataGraph.length === 1 && dataGraph[0].length === 0?
                    null:
                    <Chart
                      width={'1000px'}
                      height={'300px'}
                      style={{marginTop: '3%'}}
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
                    }
                  </div>
                  
            </form>
        </div>

	);
};

export default Statistics;
