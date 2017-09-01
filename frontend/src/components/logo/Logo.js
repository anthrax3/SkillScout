import React from 'react';

class Logo extends React.Component {
  constructor() {
    super();
    this.determineClassName = this.determineClassName.bind(this);
  }
  determineClassName() {
    if (this.props.bShowResults) {
      return "logoHidden";
    } else {
      return "logo";
    }
  }
  render() {
    return (
        <div className={this.determineClassName()}>
        <div>
          <div className="logoContainer">
            <div className="backgroundCircle"></div>
            <div className="inner">
              <div className="shadow"></div>
            </div>
            <div className="inner right">
              <div className="shadow"></div>
            </div>
            <div className="bridge"></div>
            <div className="rim"></div>
            <div className="rim right"></div>
          </div>

        </div>
        <div className="titleContainer">
          <h1 id="title">SkillScout <span className="sup">TM</span> </h1>
        </div>
        </div>
    );
  }
}

Logo.defaultProps = {
};

export default Logo;
