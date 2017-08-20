import React from 'react';

class Footer extends React.Component {
  render() {
    var sYear = new Date().getFullYear();
    return (
      // <a href="#">About</a>
      // |
      <footer>
        {'\u00a9'} SkillScout {sYear}
      </footer>
    );
  }
}

Footer.defaultProps = {
};

export default Footer;
