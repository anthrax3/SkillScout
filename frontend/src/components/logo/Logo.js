import React from 'react';

class Logo extends React.Component {
  constructor() {
    super();
    this.determineLogoClassName = this.determineLogoClassName.bind(this);
  }
  determineLogoClassName() {
    if (this.props.bShowResults) {
      return "logoFixed";
    } else {
      return "logoBlock";
    }
  }
  render() {
    return (
        <div className="logo">
        <div className={this.determineLogoClassName()}>
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
        <div className="titleContainer">
          <h1 id="title">SkillScout <span className="sup">TM</span> </h1>
        </div>
        </div>

        </div>
    );
  }
}

Logo.defaultProps = {
};

export default Logo;
