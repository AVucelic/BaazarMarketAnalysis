import BaazarApi from './components/baazarApi';
import React, { Component } from 'react';
import './App.css';

export default class App extends Component {
  render() {
    return (
      <div>
        <h1>Welcome to Baazar</h1>
        <section><BaazarApi /></section>
      </div>
    );
  }
}
