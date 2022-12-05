import { Row, Col } from 'react-bootstrap'
import React, { useState, useEffect } from 'react'
import axios from 'axios';
import ServiceCard from "../components/ServiceCard";



function HomeScreen() {
    const [post, setPost] = useState([]);
    const service = axios.get('http://localhost:8080/server_list')
    useEffect(() => {
        axios.get('http://localhost:8080/server_list').then((response) => {

            setPost(response.data);
        });
    }, []);
    console.log(post)

    return (
        <div>
            <div>
                <Row>
                    {post.map(elem=> (
                        <Col key={elem[0]} sm={15} md={7} lg={5} xl={4}>
                            <ServiceCard service={elem} />
                        </Col>
                    ))}
                </Row>
            </div>
        </div>
    )
}
export default HomeScreen
