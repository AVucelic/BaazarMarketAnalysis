import React, { Component } from 'react';
import axios from 'axios';
import './baazarApi.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';

class BaazarApi extends Component {

    constructor(props) {
        super(props);
        this.state = {
            products: {},
            isLoading: true,
            error: null
        };
    }

    componentDidMount() {
        axios.get('https://api.hypixel.net/v2/skyblock/bazaar')
            .then(res => {
                console.log(res.data); // Log the response data
                this.setState({ products: res.data.products, isLoading: false });
            })
            .catch(error => {
                console.log(error);
                this.setState({ error, isLoading: false });
            });
    }

    render() {
        const { products, isLoading, error } = this.state;
        if (isLoading) {
            return <div>Loading...</div>;
        }
        if (error) {
            return <div>Error: {error.message}</div>;
        }
        return (
            <div>
                {Object.keys(products).map(productId => {
                    const product = products[productId];
                    const sellSummary = product.sell_summary;
                    const buySummary = product.buy_summary;
                    const quickStatus = product.quick_status;

                    return (
                        <Card key={productId}>
                            <CardContent>
                                <h2>{productId}</h2>
                                <h3>Sell Summary:</h3>
                                {sellSummary.map((sell, index) => (
                                    <div key={index}>
                                        <p>Amount: {sell.amount}</p>
                                        <p>Price per Unit: {sell.pricePerUnit}</p>
                                        <p>Orders: {sell.orders}</p>
                                    </div>
                                ))}
                                <h3>Buy Summary:</h3>
                                {buySummary.map((buy, index) => (
                                    <div key={index}>
                                        <p>Amount: {buy.amount}</p>
                                        <p>Price per Unit: {buy.pricePerUnit}</p>
                                        <p>Orders: {buy.orders}</p>
                                    </div>
                                ))}
                                <h3>Quick Status:</h3>
                                <div>
                                    <p>Sell Price: {quickStatus.sellPrice}</p>
                                    <p>Sell Volume: {quickStatus.sellVolume}</p>
                                    <p>Sell Orders: {quickStatus.sellOrders}</p>
                                    <p>Buy Price: {quickStatus.buyPrice}</p>
                                    <p>Buy Volume: {quickStatus.buyVolume}</p>
                                    <p>Buy Orders: {quickStatus.buyOrders}</p>
                                </div>
                            </CardContent>
                            <CardActions>
                                <button>Buy</button>
                            </CardActions>
                        </Card>
                    );
                })}
            </div>
        );
    }
}

export default BaazarApi;
