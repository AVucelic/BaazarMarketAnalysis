import React, { Component } from 'react';
import axios from 'axios';
import './baazarApi.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';

const API_KEY = '202ac6ab-0414-465c-8c7c-b976bad32f74';

class BaazarApi extends Component {
    constructor(props) {
        super(props);
        this.state = {
            products: {},
            productNames: {},
            isLoading: true,
            error: null,
            visibleItems: 10 // Number of items initially visible
        };
    }

    componentDidMount() {
        axios.get(`https://api.hypixel.net/v2/skyblock/bazaar?key=${API_KEY}`)
            .then(res => {
                this.setState({ products: res.data.products });
                return axios.get(`https://api.hypixel.net/v2/resources/skyblock/items?key=${API_KEY}`);
            })
            .then(res => {
                if (res.data && Array.isArray(res.data.items)) {
                    const productNames = {};
                    res.data.items.forEach(item => {
                        productNames[item.id] = item.name;
                    });
                    this.setState({ productNames, isLoading: false });
                } else {
                    throw new Error('Invalid format for product names response');
                }
            })
            .catch(error => {
                console.error(error);
                this.setState({ error, isLoading: false });
            });
    }

    // Handler to show more items
    showMoreItems = () => {
        this.setState(prevState => ({
            visibleItems: prevState.visibleItems + 10 // Increase visible items by 10
        }));
    }

    render() {
        const { products, productNames, isLoading, error, visibleItems } = this.state;

        if (isLoading) {
            return <div>Loading...</div>;
        }
        if (error) {
            return <div>Error: {error.message}</div>;
        }

        // Get the list of product IDs and limit it based on visibleItems
        const productIds = Object.keys(products).filter(productId =>
            !productId.startsWith('ENCHANTMENT') && !productId.startsWith('ESSENCE')
        );
        const visibleProductIds = productIds.slice(0, visibleItems);

        return (
            <div className="products-container">
                {visibleProductIds.map(productId => {
                    const product = products[productId];
                    const quickStatus = product.quick_status;
                    const productName = productNames[productId] || productId;

                    return (
                        <Card key={productId} className="product-card">
                            <CardContent>
                                <h2>{productName}</h2>
                                <h3>Quick Status:</h3>
                                <div className="quick-status">
                                    <p>Sell Price: {quickStatus.sellPrice}</p>
                                    <p>Sell Volume: {quickStatus.sellVolume}</p>
                                    <p>Sell Orders: {quickStatus.sellOrders}</p>
                                    <p>Buy Price: {quickStatus.buyPrice}</p>
                                    <p>Buy Volume: {quickStatus.buyVolume}</p>
                                    <p>Buy Orders: {quickStatus.buyOrders}</p>
                                </div>
                            </CardContent>
                            <CardActions>
                                <button>Show graph</button>
                            </CardActions>
                        </Card>
                    );
                })}
                {visibleProductIds.length < productIds.length && (
                    <div className="show-more-container">
                        <button className="show-more-button" onClick={this.showMoreItems}>
                            Show more items
                        </button>
                    </div>
                )}
            </div>
        );
    }
}

export default BaazarApi;
