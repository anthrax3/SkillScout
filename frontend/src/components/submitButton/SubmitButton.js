import React from 'react';

class SubmitButton extends React.Component {
  render() {
    return (
      <button className="submitButton" onClick={this.props.onSubmit}>{this.props.submitButtonText}</button>
    );
  }
}

SubmitButton.defaultProps = {
};

export default SubmitButton;
