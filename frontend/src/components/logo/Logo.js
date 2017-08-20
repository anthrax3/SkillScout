import React from 'react';

class Logo extends React.Component {
  render() {
    return (
      <div className="logoBlock">
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
    );
  }
}

Logo.defaultProps = {
};

export default Logo;
