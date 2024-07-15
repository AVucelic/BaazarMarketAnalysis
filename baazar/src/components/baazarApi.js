import React, { Component } from 'react';
import axios from 'axios';
import './baazarApi.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';

class baazarApi extends Component {

    constructor(props) {
        super(props);
        this.state = {
        items: []
        };
    }
    
    componentDidMount() {
        axios.get('https://baazarapi.herokuapp.com/api/items')
        .then(res => {
            this.setState({ items: res.data });
        })
        .catch(function (error) {
            console.log(error);
        });
    }
    
    render() {
        return (
        <div>
            {this.state.items.map(item =>
            <Card key={item.id}>
                <CardContent>
                <h2>{item.name}</h2>
                <p>{item.description}</p>
                <p>Price: {item.price}</p>
                </CardContent>
                <CardActions>
                <button>Buy</button>
                </CardActions>
            </Card>
            )}
        </div>
        );
    }
}