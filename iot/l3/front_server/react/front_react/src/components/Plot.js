import React, { useState, useEffect } from 'react'
import axios from 'axios';
import ApexCharts from 'apexcharts'
import Chart from "react-apexcharts";


function Plot({ name }) { 
    const [isLoading, setLoading] = useState(true);
    const [post, setPost] = useState([]);
    console.log(name);
    // const service = axios.get('http://localhost:8080/server_list')
    useEffect(() => {
        console.log("test");
        axios.get('http://0.0.0.0:8083/ohlc?instrument='+name+'&time_unit=hour&time_val=1').then((response) => {
            setPost(response.data);
            setLoading(false);
        });
    }, []);
  console.log(post.values);
  if (isLoading) {
    return <div className="App">Loading...</div>;
  };

  var data = []
  post.values.map(x => {
    data.push({
      x: new Date(x[0]),
      y: x[1]
    })
  });
  var series = [{
    data: data
  }]
  var options = {
              chart: {
                type: 'candlestick',
                height: 350
              },
              title: {
                text: 'CandleStick Chart',
                align: 'left'
              },
              xaxis: {
                type: 'datetime'
              },
              yaxis: {
                tooltip: {
                  enabled: true
                }
              }
            };


return (
  <div id = "chart">
      <Chart 
        options={options}
        series={series}
        type="candlestick"
        />
    </div>
  )
}

export default Plot
