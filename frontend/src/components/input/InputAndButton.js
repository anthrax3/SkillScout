import React from 'react';

import Geosuggest from 'react-geosuggest';
import {notify} from 'react-notify-toast';

let oCustomStyle = { background: '#FF5714', text: "#E4FF1A" }; // red-orange background, yellow text

class Input extends React.Component {
  constructor(){
    super();
    this.onSuggestSelect = this.onSuggestSelect.bind(this);
  }
  // this should fire when: enter is pressed, a suggest is selected, OR button is pressed (need to test)
  onSuggestSelect(suggest) {
    console.log(suggest);
    if (suggest.gmaps) {
      this.props.onSubmit(suggest.gmaps.place_id);
    } else {
      notify.show("Location could not be found! Care to try again?", "custom", 5000, oCustomStyle);
    }
  }
  render() {
    return (
      <div>
        <div id="input">
          <div id="input--orangeBorder">
            <div id="input--yellowBorder">
              <Geosuggest ref={el=>this._geoSuggest=el} placeholder="Search for a city..." onSuggestSelect={this.onSuggestSelect} />
            </div>
          </div>
        </div>
        <button className="submitButton" onClick={()=>this._geoSuggest.selectSuggest()}>{this.props.submitButtonText}</button>
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
