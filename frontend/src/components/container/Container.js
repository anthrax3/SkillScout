import React from 'react';

class Input extends React.Component {
  constructor() {
    super()
    this.determineClassName = this.determineClassName.bind(this);
  }
  determineClassName() {
    if (this.props.bShowResults) {
      return "container--noBorder";
    } else {
      console.log("container--border...");
      return "container--border";
    }
  }
  render() {
    return (
      <div className={this.determineClassName()}>
        {this.props.children}
      </div>
    );
  }
}

Input.defaultProps = {
};

export default Input;
