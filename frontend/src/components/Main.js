require('normalize.css/normalize.css');
require('styles/App.css');

// third party components
import React from 'react';
import Popup from 'react-popup';
import Notifications from 'react-notify-toast';

// custom components
import SearchErrorPopupContent from './popups/SearchErrorPopupContent.js'
import Container from './container/Container.js';
import Background from './background/Background.js';
import Logo from './logo/Logo.js';
import InputGuide from './inputGuide/InputGuide.js';
import InputAndButton from './input/InputAndButton.js';
import Results from './results/Results.js';
import Footer from './footer/Footer.js';

// constants TODO: should eventually be moved to a CONSTS file
const sNewSearchText = 'NEW SEARCH!';


class AppComponent extends React.Component {
  constructor() {
      super();
      this.state = {
        bShowResults: false,
        submitButtonText: 'GO!',
        placeId: ''
      };
      //this.onChange = this.onChange.bind(this);
      this.onSubmit = this.onSubmit.bind(this);
      this.onClickCityError = this.onClickCityError.bind(this);
  }
  onSubmit(placeId) {
    this.setState({placeId: placeId, bShowResults: true, submitButtonText: sNewSearchText});
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
  render() {
    // <Background/>

    return (
      <div>
        <Notifications />
        <Container bShowResults={this.state.bShowResults}>
          <Logo bShowResults={this.state.bShowResults}/>
          { !this.state.bShowResults && <InputGuide/>}
          <InputAndButton onSubmit={this.onSubmit} submitButtonText={this.state.submitButtonText}/>
          { this.state.bShowResults && <Results placeId={this.state.placeId} onClickCityError={this.onClickCityError}/> }
          <Footer/>
        </Container>
      </div>
    );
  }
}

AppComponent.defaultProps = {
};

export default AppComponent;
