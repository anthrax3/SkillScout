import React from 'react';

import Geosuggest from 'react-geosuggest';

class Input extends React.Component {
  constructor(){
    super();
    this.state = {
      city: ''
    }
    this.handleInputKeyPress = this.handleInputKeyPress.bind(this);
    this.handleSuggestSelect = this.handleSuggestSelect.bind(this);
    this.handleButtonClick = this.handleButtonClick.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
  }
  handleInputKeyPress = (e) => {
    if (e.key === 'Enter') {
      //console.log(e.target.value);
      this.props.onSubmit(this.state.city); // send the city up to main
    }
  }
  handleSuggestSelect(suggest) {
    this.setState({city: suggest.label});
    this.props.onSubmit(suggest.label)
  }
  handleButtonClick() {
    this.props.onSubmit(this.state.city);
  }
  handleOnChange = (val) => {
    console.log(val);
    this.setState({city: val});
  }
  render() {
    return (
      <div>
        <div id="input">
          <div id="input--orangeBorder">
            <div id="input--yellowBorder">
              <Geosuggest onKeyPress={this.handleInputKeyPress} placeholder="Search cities..." onChange={this.handleOnChange} onSuggestSelect={this.handleSuggestSelect} ref={(input) => { this.geoInput = input; }} />
            </div>
          </div>
        </div>
        <button className="submitButton" onClick={this.handleButtonClick}>{this.props.submitButtonText}</button>
      </div>
    );
  }
  componentDidMount(){
    this.geoInput.focus();
  }
}

Input.defaultProps = {
};

export default Input;
