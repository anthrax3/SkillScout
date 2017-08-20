import React from 'react';

import Geosuggest from 'react-geosuggest';

class Input extends React.Component {
  constructor(){
    super();
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleOnChange = this.handleOnChange.bind(this);
  }
  handleSubmit = (e) => {
    if (e.key === 'Enter') {
      console.log(e.target.value);
      this.props.onSubmit(e.target.value);
    }
  }
  handleOnChange = (val) => {
    console.log(val);
    this.props.onChange(val);
  }
  render() {
    return (
      // <input type="text" name="locationText" id="location" data-fav="location-icon" autocomplete="off">
      // onKeyPress={this._handleKeyPress}
      <div>
        <div id="input">
          <div id="input--orangeBorder">
            <div id="input--yellowBorder">
              <Geosuggest onKeyPress={this.handleSubmit} placeholder="Search cities..." onChange={this.handleOnChange}/>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

Input.defaultProps = {
};

export default Input;
