import baazarApi from './components/baazarApi';
import React, { Component } from 'react';
import React from 'react';
import './App.css';

export default class App extends React.Component {
  render() {
    return (
      <div>
        <h1>Welcome to Baazar</h1>
        <section><baazarApi /></section>
      </div>
    );
  }
}