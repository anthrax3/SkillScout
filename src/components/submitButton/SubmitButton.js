import React from 'react';

class SubmitButton extends React.Component {
  render() {
    return (
      <button className="submitButton" onClick={this.props.onSubmit}>GO!</button>
    );
  }
}

SubmitButton.defaultProps = {
};

export default SubmitButton;
