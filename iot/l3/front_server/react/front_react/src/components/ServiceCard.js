import React from "react";
import {Button, Card, ListGroup} from 'react-bootstrap'
import Container from "../Container";
import axios from "axios";

function ServiceCard({ service }) {
    const triggerText = 'Edit';
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
        </ListGroup>
            <Container triggerText={triggerText} onSubmit={onSubmit} data={service}/>
        </Card>
    )
}

export default ServiceCard