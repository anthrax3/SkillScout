import React from 'react';

class Input extends React.Component {
  render() {
    return (
      <div id="container">
        {this.props.children}
      </div>
    );
  }
}

Input.defaultProps = {
};

export default Input;
