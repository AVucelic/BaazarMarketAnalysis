import React, { Component } from 'react';
import Home from './components/Home';
import BaazarApi from './components/baazarApi';
import './App.css';

export default class App extends Component {
  constructor(props) {
    super(props);
    this.baazarRef = React.createRef(); // Create a ref for the BaazarApi section
  }

  render() {
    return (
      <div className="app-container">
        <section className="home-section">
          <Home />
        </section>
        <section className="baazar-api-section" ref={this.baazarRef}>
          <BaazarApi />
        </section>
      </div>
    );
  }
}
