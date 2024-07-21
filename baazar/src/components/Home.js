import React, { Component } from 'react';
import './Home.css';

class Home extends Component {
    scrollToBaazar = () => {
        const element = document.querySelector('.baazar-api-section');
        if (element) {
            element.scrollIntoView({ behavior: 'smooth' });
        }
    };

    render() {
        return (
            <div className="home-container">
                <div className="welcome-text">
                    <h1>Welcome to the Baazar</h1>
                    <button onClick={this.scrollToBaazar}>
                        Go to Baazar
                    </button>
                </div>
            </div>
        );
    }
}

export default Home;
