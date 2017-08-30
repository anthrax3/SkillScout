import 'core-js/fn/object/assign';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/Main';

var firebase = require('firebase/app');
require('firebase/auth');
require('firebase/database');

// Initialize Firebase
var config = {
  apiKey: "AIzaSyBUtf-GRN-A9aZuS6eFITOlY4CLXK1nzD8",
  authDomain: "skillscout-123.firebaseapp.com",
  databaseURL: "https://skillscout-123.firebaseio.com",
  projectId: "skillscout-123",
  storageBucket: "skillscout-123.appspot.com",
  messagingSenderId: "764003056781"
};
firebase.initializeApp(config);
  
// Render the main component into the dom
ReactDOM.render(<App />, document.getElementById('app'));
