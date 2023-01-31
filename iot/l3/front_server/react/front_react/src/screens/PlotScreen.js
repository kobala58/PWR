import { Row, Col } from 'react-bootstrap'
import React, { useState, useEffect } from 'react'
import axios from 'axios';
import Plot from '../components/Plot';

function PlotScreen(){
    const [post, setPost] = useState([]);
    // const service = axios.get('http://localhost:8080/server_list')
    useEffect(() => {
        axios.get('http://0.0.0.0:8083/').then((response) => {
            setPost(response.data);
            console.log(response);
        });
    }, []);

    return (
        <div>
            <div>
                <Row>
                    {post.map(elem=> (
                      <div id={"chart"+elem.walor}>
                      <Plot name={elem.walor}/>
                      </div>
                    ))}
                </Row>
            </div>
        </div>
    )
}

export default PlotScreen
