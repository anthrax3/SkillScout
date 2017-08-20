require('normalize.css/normalize.css');
require('styles/App.css');

import React from 'react';

// custom components
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
        sLocation: '',
        aJobData: {percChangeMonth: -5,
        leadDescription: 'Developer',
      leadSkill1: 'Webscraping',
    leadSkill1Perc: 32}
      };
      this.onChange = this.onChange.bind(this);
      this.onSubmit = this.onSubmit.bind(this);
      this.loadResults = this.loadResults.bind(this);
  }
  onChange(sLocation) {
    console.log(sLocation);
    this.setState({sLocation: sLocation});
  }
  onSubmit(sLocation) {
    console.log(sLocation);
      this.setState({sLocation: sLocation});
      this.loadResults();
  }
  loadResults() {
    // TODO: on select from drop down are NOT propagating to the sLocation portion of the state
    console.log('getting results for:');
    console.log(this.state.sLocation);
    this.setState({bShowResults: true});
//     this.setState({aJobData: [{percChangeMonth: -5,
//     leadDescription: 'Developer',
//   leadSkill1: 'Webscraping',
// leadSkill1Perc: 32}]});
    // fetch process will look something like this:
    // fetch(sLocation).then(function(response) {
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
        { this.state.bShowResults && <Results jobData={this.state.aJobData} city={this.state.sLocation}/> }
        <Footer/>
      </Container>
    );
  }
}

AppComponent.defaultProps = {
};

export default AppComponent;
