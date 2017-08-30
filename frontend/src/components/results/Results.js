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
      sLastSearchedCity: '',
      sSelectedFilter: 'Select...',
      writtenDescriptionData: {},
      doughnutChartData: {},
      recentTrendsChartData: {},
      longTrendsChartData: {},
      bResultsFound: true
    };
    this.onClickDropdown = this.onClickDropdown.bind(this);
    this.onClickCityError = this.onClickCityError.bind(this);
    this.onClickGoToCityPage = this.onClickGoToCityPage.bind(this);
    this.clearResults = this.clearResults.bind(this);
    this.getResults = this.getResults.bind(this);
  }
  onClickDropdown(sField) {
    console.log(sField);
    this.setState({sSelectedFilter: sField});
  }
  onClickGoToCityPage() {
    // TODO: react router stuff (open the city page)
    window.open('localhost:8000/cityList.html')
  }
  onClickCityError() {
    this.props.onClickCityError;
  }
  clearResults() {
    this.setState({writtenDescriptionData: {}, doughnutChartData: {}, recentTrendsChartData: {}, longTrendsChartData: {}});
  }
  getResults() {
    console.log("getResults()...");
    console.log(this.props.city);
    if (this.state.sLastSearchedCity !== this.props.city) {
      var that = this;
      var sCity = this.props.city;
      console.log(sCity);
      return firebase.database().ref('/' + sCity + '/').once('value').then(function(snapshot) {
        var oData = snapshot.val();
        if (oData !== null) {
          that.setState({
              writtenDescriptionData: oData.writtenDescriptionData,
              doughnutChartData: oData.doughnutChartData,
              recentTrendsChartData: oData.recentTrendsChartData,
              longTrendsChartData: oData.longTrendsChartData,
              sLastSearchedCity: sCity,
              bResultsFound: true
          });
        } else {
          console.log("results not found!");
            that.setState({sLastSearchedCity: sCity, bResultsFound: false});
          }
      });
    }
  }
  componentWillMount() {
    console.log("componentWillMount()...");
    console.log(this.props.city);
    this.getResults(); // before the very first render, try to get the data associated with the city
  }
  render() {
    // determine direction based on percentage change value
    var writtenDescriptionData = this.state.writtenDescriptionData;
    var direction = writtenDescriptionData.percChangeMonth > 0 ? 'up' : 'down';

    return (
      <div>
        { this.state.bResultsFound &&
          <div id="results">
            <h2>Trending job skills for<br/><span className="coolCity">{this.props.city}</span><br/><a href="#" className="cityErrorText" onClick={this.onClickCityError}>(Why are you showing me this city?)</a></h2>
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
              <h2>Trendings Skills in {this.props.city} (Past 3 Months)</h2>
                <RecentTrendsChart recentTrendsChartData={this.state.recentTrendsChartData}/>
              <h2>Trendings Skills in {this.props.city} (Past Year)</h2>
                <LongTrendsChart longTrendsChartData={this.state.longTrendsChartData}/>
              <h2>Filters</h2>
                Show me relevant skills for:
                <JobsDropdown selectedFilter={this.state.selectedFilter} onClickDropdown={this.onClickDropdown}/>
              </div>
          </div>
        }
        { !this.state.bResultsFound &&
          <div id="results">
            <h2>Sorry, no results were found for {this.props.city} :(<br/><a href="#" className="cityErrorText" onClick={this.onClickCityError}>(Why?)</a></h2>
          </div>
        }
      </div>
    );
  }
  componentDidUpdate() {
    // TODO: put this stuff in the component did mount, have a loader rendering in the meanwhile yahoooo
    console.log("componentDidUpdate()...");
    console.log(this.props.city);
    this.getResults();
  }
}

Results.defaultProps = {
};

export default Results;
