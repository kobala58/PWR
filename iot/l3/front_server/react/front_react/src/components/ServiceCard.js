import React, { useEffect, useState } from "react";
import {Button, Card, ListGroup, ListGroupItem} from 'react-bootstrap'
import Container from "../Container";
import axios from "axios";

function ServiceCard({ service }) {
    function checkOnline(){    
      axios.get('http://localhost:'+service[9]+'/').then((response) => {
      console.log(response);
      if(response.status == 200){
        console.log("req_sie_zgada");
        setResp(true);
      }else{
        setResp(false);
      }
    });
  }  

    const [res, setResp] = useState(Boolean);
    let online = false

    useEffect(() => {
      axios.get('http://localhost:'+service[9]+'/').then((response) => {
      console.log(response);
      if(response.status == 200){
        console.log("req_sie_zgada");
        setResp(true);
      }else{
        setResp(false);
      }
    });
  }, []);
    
  console.log(res);
    const triggerText = 'Edit';
    const replicate = "Replicate";
    const onSubmit = (event) => {
        event.preventDefault(event);
        axios({
            method: 'post',
            url: 'http://localhost:8080/change_config/'+event.target.name.value,
            data: {
                svr_id: event.target.svr_id.value,
                method: event.target.method.value,
                port: event.target.port.value,
                interval: event.target.interval.value,
                source: event.target.source.value,
                channel: event.target.channel.value,
                server: event.target.server.value
            }
        }).then(function (response) {
            console.log(response);
        })
    };
  
    const createEmpty = (event) => {
        event.preventDefault(event);
        axios({
            method: 'post',
            url: 'http://localhost:8080/create_empty',
            data: {
                name: event.target.name.value,
                method: event.target.method.value,
                port: event.target.port.value,
                interval: event.target.interval.value,
                source: event.target.source.value,
                channel: event.target.channel.value,
                server: event.target.server.value
            }
        }).then(function (response) {
            console.log(response);
        })
    };
    const createNew = (event) => {
        event.preventDefault(event);
        axios({
            method: 'post',
            url: 'http://localhost:8080/create_new',
            data: {
                name: event.target.name.value,
                method: event.target.method.value,
                port: event.target.port.value,
                interval: event.target.interval.value,
                source: event.target.source.value,
                channel: event.target.channel.value,
                server: event.target.server.value
            }
        }).then(function (response) {
            console.log(response);
        })
    };
    return (
        <Card className={"my-2 p-2 rounded"}>
            <Card.Header>{service[1]}</Card.Header>
            <Card.Body>
                <Card.Title>{service[5]}</Card.Title>
            </Card.Body>
            <ListGroup className="list-group-flush">
            <ListGroup.Item>ID: {service[0]}</ListGroup.Item>
            <ListGroup.Item>METHOD: {service[2]}</ListGroup.Item>
            <ListGroup.Item>PORT: {service[3]}</ListGroup.Item>
            <ListGroup.Item>INTERVAL: {service[4]}</ListGroup.Item>
            <ListGroup.Item>DATA ENDPOINT: "{service[6]}"</ListGroup.Item>
            <ListGroup.Item>IP ENDPOINT: {service[7]}</ListGroup.Item>
            <ListGroup.Item>PORT on localhost: {service[9]}</ListGroup.Item>
            <ListGroup.Item>Ping: {res === true ? "green": "red"}</ListGroup.Item>
            <ListGroup.Item><Button onClick={() => checkOnline()}>Ping</Button></ListGroup.Item>
            <ListGroup.Item> 
                <Container triggerText={triggerText} onSubmit={onSubmit} data={service}/>
            </ListGroup.Item>

            <ListGroup.Item> 
                <Container triggerText={"Create Without Docker"} onSubmit={createEmpty} data={service}/>
            </ListGroup.Item>
            <ListGroup.Item> <Container triggerText={replicate} onSubmit={createNew} data={service}/></ListGroup.Item>  
      </ListGroup>
        </Card>
    )
}

export default ServiceCard
