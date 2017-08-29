import React from 'react';

const aFields = ["Computers / Technology", "Health Care / Allied Health", "Education / Social Services", "Arts / Communications", "Trades / Transportation", "Management / Business, / Finance", "Architecture / Civil Engineering", "Science", "Hospitality, Tourism, / the Service Industry", "Law / Law Enforcement"];

class JobsDropdown extends React.Component {
  constructor() {
    super();
  }
  render() {
    var aDropDownFields = [];
    aFields.forEach((sField, iIndex) => {
      aDropDownFields.push(<a key={iIndex} href="#" onClick={() => this.props.onClickDropdown(sField)}>{sField}</a>);
    });
    console.log(this.props.selectedFilter);
    return (
      <div className="dropdown">
        <button className="dropbtn">{this.props.selectedFilter}</button>
        <div className="dropdown-content">
          {aDropDownFields}
        </div>
      </div>
    );
  }
}

JobsDropdown.defaultProps = {
};

export default JobsDropdown;
