require('normalize.css/normalize.css');
require('styles/App.css');

import React from 'react';
import Popup from 'react-popup';

// custom components
import SearchErrorPopupContent from './popups/SearchErrorPopupContent.js'
import Container from './container/Container.js';
import Background from './background/Background.js';
import Logo from './logo/Logo.js';
import Title from './title/Title.js';
import InputGuide from './inputGuide/InputGuide.js';
import Input from './input/Input.js';
import SubmitButton from './submitButton/SubmitButton.js';
import Results from './results/Results.js';
import Footer from './footer/Footer.js';

class AppComponent extends React.Component {
  constructor() {
      super();
      this.state = {
        bShowResults: false,
        city: ''
      };
      this.onChange = this.onChange.bind(this);
      this.onSubmit = this.onSubmit.bind(this);
      this.loadResults = this.loadResults.bind(this);
      this.onClickCityError = this.onClickCityError.bind(this);
  }
  onChange(city) {
    console.log(city);
    this.setState({city: city});
  }
  onSubmit(city) {
    console.log(city);
      this.setState({city: city, bShowResults: true});
      //this.loadResults();
  }
  onClickCityError() {
    console.log("in onClickCityError...");
    Popup.create({
      title: null,
      content: <SearchErrorPopupContent/>,
      className: 'alert',
      buttons: {
          right: ['Done']
      }
    });
  }
  loadResults() {
    // TODO: on select from drop down are NOT propagating to the city portion of the state
    console.log('getting results for:');
    console.log(this.state.city);
    this.setState({bShowResults: true});
//     this.setState({aJobData: [{percChangeMonth: -5,
//     leadDescription: 'Developer',
//   leadSkill1: 'Webscraping',
// leadSkill1Perc: 32}]});
    // fetch process will look something like this:
    // fetch(city).then(function(response) {
    //   response.json().then(function(data) {
    //     // do something with your data
    //     this.setState({oData: data})
    //   });
    // });
  }
  render() {
    return (
      <Container>
        <Background/>
        { !this.state.bShowResults && <Logo/> }
        { !this.state.bShowResults && <Title/> }
        { !this.state.bShowResults && <InputGuide/>}
        <Input onSubmit={this.onSubmit} onChange={this.onChange}/>
        <SubmitButton onSubmit={this.loadResults}/>
        { this.state.bShowResults && <Results city={this.state.city} onClickCityError={this.onClickCityError}/> }
        <Footer/>
      </Container>
    );
  }
}

AppComponent.defaultProps = {
};

export default AppComponent;
