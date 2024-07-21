import React, { Component } from 'react';
import axios from 'axios';
import './baazarApi.css';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';

const API_KEY = '27a7a87a-3ed9-4831-a2de-dc7fbb014b9f';

class BaazarApi extends Component {
    constructor(props) {
        super(props);
        this.state = {
            products: {},
            productNames: {},
            isLoading: true,
            error: null,
            visibleItems: 10,
            sortOrder: 'desc', 
            sortKey: 'sellPrice' 
        };
        this.interval = null;  
    }

    fetchData = () => {
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

    componentDidMount() {
        this.fetchData(); 
        this.interval = setInterval(this.fetchData, 60000); 
    }

    componentWillUnmount() {
        if (this.interval) {
            clearInterval(this.interval); 
        }
    }

    showMoreItems = () => {
        this.setState(prevState => ({
            visibleItems: prevState.visibleItems + 10
        }));
    }

    handleSortChange = (event) => {
        const [key, order] = event.target.value.split(',');
        this.setState({ sortKey: key, sortOrder: order });
    }

    render() {
        const { products, productNames, isLoading, error, visibleItems, sortOrder, sortKey } = this.state;

        if (isLoading) {
            return <div>Loading...</div>;
        }
        if (error) {
            return <div>Error: {error.message}</div>;
        }

        const productIds = Object.keys(products).filter(productId =>
            !productId.startsWith('ENCHANTMENT') && !productId.startsWith('ESSENCE')
        );

        const sortedProductIds = productIds.sort((a, b) => {
            const valueA = products[a].quick_status[sortKey];
            const valueB = products[b].quick_status[sortKey];
            return sortOrder === 'asc' ? valueA - valueB : valueB - valueA;
        });

        const visibleProductIds = sortedProductIds.slice(0, visibleItems);

        return (
            <div>
                <div className="sort-dropdown-container">
                    <span>Sort By: </span>
                    <select className="sort-dropdown" onChange={this.handleSortChange}>
                        <option value="sellPrice,desc">Sell Price (Descending)</option>
                        <option value="sellPrice,asc">Sell Price (Ascending)</option>
                        <option value="buyPrice,desc">Buy Price (Descending)</option>
                        <option value="buyPrice,asc">Buy Price (Ascending)</option>
                        <option value="sellVolume,desc">Sell Volume (Descending)</option>
                        <option value="sellVolume,asc">Sell Volume (Ascending)</option>
                        <option value="buyVolume,desc">Buy Volume (Descending)</option>
                        <option value="buyVolume,asc">Buy Volume (Ascending)</option>
                    </select>
                </div>
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
                                        <p>Sell Price: {quickStatus.sellPrice.toFixed(1)}</p>
                                        <p>Sell Volume: {quickStatus.sellVolume}</p>
                                        <p>Sell Orders: {quickStatus.sellOrders}</p>
                                        <p>Buy Price: {quickStatus.buyPrice.toFixed(1)}</p>
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
            </div>
        );
    }
}

export default BaazarApi;
