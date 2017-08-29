import React from 'react';

class SearchErrorPopupContent extends React.Component {
  render() {
    return (
      <p>We may not support the city you are looking for yet, or your search was too broad. <a href="#" onClick={this.onClickGoToCityPage()}>Click here to see a list of cities SkillScout supports.</a> Or, <a href="#" onClick={this.onClickSearchAgain()}>try searching again.</a></p>
    );
  }
}

SearchErrorPopupContent.defaultProps = {
};

export default SearchErrorPopupContent;
