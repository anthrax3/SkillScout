import React from 'react';

class Results extends React.Component {
  constructor() {
    super();
    this.state = {
      sSelectedFilter: 'Select...'
    };
    this.onClickDropdown = this.onClickDropdown.bind(this);
  }
  onClickDropdown = (e) => {
    this.setState({sSelectedFilter: e.target.value});
  }
  render() {
    // determine direction based on percentage change value
    var oJobData = this.props.jobData;
    var direction = oJobData.percChangeMonth > 0 ? 'up' : 'down';

    return (
      <div id="results">
        <h2>Trending job skills for {this.props.city}:</h2>
        <div className="reportContainer">
          <h2>Overview</h2>
          <h4>Key Points</h4>
          <ul className="keyPointsList">
            <li>{this.props.city} jobs are <b>{direction} {oJobData.percChangeMonth}%</b> since last month.</li><br/>
            <li><b>{oJobData.leadDescription}</b> is the most desired job description. The most desired skill for this job is <b>{oJobData.leadSkill1}</b> (<b>{oJobData.leadSkill1Perc}%</b> of postings)</li><br/>
            <li>Something...</li><br/>
            <li>Something more...</li><br/>
                    </ul>
          <h2>Job offer distribution</h2>
          <p>(Pie Chart Coming Soon)</p>
          <h2>Filters</h2>
          Show me relevant skills for:
          <div className="dropdown">
            <button className="dropbtn">{this.state.selectedFilter}</button>
            <div className="dropdown-content">
              <a href="#" onClick={this.onClickDropdown}>Computers / Technology</a>
              <a href="#" onClick={this.onClickDropdown}>Health Care / Allied Health</a>
              <a href="#" onClick={this.onClickDropdown}>Education / Social Services</a>
              <a href="#" onClick={this.onClickDropdown}>Arts / Communications</a>
              <a href="#" onClick={this.onClickDropdown}>Trades / Transportation</a>
              <a href="#" onClick={this.onClickDropdown}>Management / Business, / Finance</a>
              <a href="#" onClick={this.onClickDropdown}>Architecture / Civil Engineering</a>
              <a href="#" onClick={this.onClickDropdown}>Science</a>
              <a href="#" onClick={this.onClickDropdown}>Hospitality, Tourism, / the Service Industry</a>
              <a href="#" onClick={this.onClickDropdown}>Law / Law Enforcement</a>
                </div>
              </div>
            </div>
        </div>

    );
  }
}

Results.defaultProps = {
};

export default Results;
