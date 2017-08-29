import React from 'react';

import JobsDropdown from './JobsDropdown.js';
import DoughnutChart from '../charts/DoughnutChart.js';
import RecentTrendsChart from '../charts/RecentTrendsChart';
import LongTrendsChart from '../charts/LongTrendsChart';

var firebase = require('firebase/app');

class Results extends React.Component {
  constructor() {
    super();
    this.state = {
      sSelectedFilter: 'Select...',
      writtenDescriptionData: {},
      doughnutChartData: {},
      recentTrendsChartData: {},
      longTrendsChartData: {}
    };
    this.onClickDropdown = this.onClickDropdown.bind(this);
    this.onClickCityError = this.onClickCityError.bind(this);
    this.onClickGoToCityPage = this.onClickGoToCityPage.bind(this);
    this.onClickSearchAgain = this.onClickSearchAgain.bind(this);
  }
  onClickDropdown(sField) {
    console.log(sField);
    this.setState({sSelectedFilter: sField});
  }
  onClickGoToCityPage() {
    // TODO: react router stuff (open the city page)
  }
  onClickSearchAgain() {

  }
  onClickCityError() {
    this.props.onClickCityError;
  }
  componentWillMount() {
    // TODO: put this stuff in the component did mount, have a loader rendering in the meanwhile yahoooo
    console.log(this.props.city);
    var that = this;
    return firebase.database().ref('/' + this.props.city + '/').once('value').then(function(snapshot) {
      var oData = snapshot.val();
      console.log(oData);
      that.setState({writtenDescriptionData: oData.writtenDescriptionData, doughnutChartData: oData.doughnutChartData, recentTrendsChartData: oData.recentTrendsChartData, longTrendsChartData: oData.longTrendsChartData});
    });
  }
  render() {
    // determine direction based on percentage change value
    var writtenDescriptionData = this.state.writtenDescriptionData;
    var direction = writtenDescriptionData.percChangeMonth > 0 ? 'up' : 'down';

    return (
      <div id="results">
        <h2>Trending job skills for {this.props.city} <a href="#" className="cityErrorText" onClick={this.onClickCityError}>(Not the correct city?)</a>:</h2>
        <div className="reportContainer">
          <h2>Overview</h2>
          <h4>Key Points</h4>
          <ul className="keyPointsList">
            <li>{this.props.city} jobs are <b>{direction} {writtenDescriptionData.percChangeMonth}%</b> since last month.</li><br/>
            <li><b>{writtenDescriptionData.leadDescription}</b> is the most desired job description. The most desired skill for this job is <b>{writtenDescriptionData.leadSkill}</b> (<b>{writtenDescriptionData.leadSkillPerc}%</b> of postings)</li><br/>
            <li>Something...</li><br/>
            <li>Something more...</li><br/>
          </ul>
          <h2>Jobs by Industry</h2>
            <DoughnutChart doughnutChartData={this.state.doughnutChartData}/>
          <h2>Trendings Skills (Past 3 Months)</h2>
            <RecentTrendsChart recentTrendsChartData={this.state.recentTrendsChartData}/>
          <h2>Trendings Skills (Past Year)</h2>
            <LongTrendsChart longTrendsChartData={this.state.longTrendsChartData}/>
          <h2>Filters</h2>
            Show me relevant skills for:
            <JobsDropdown selectedFilter={this.state.selectedFilter} onClickDropdown={this.onClickDropdown}/>
          </div>
        </div>
    );
  }
}

Results.defaultProps = {
};

export default Results;
