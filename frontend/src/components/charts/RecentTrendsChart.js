import React from 'react';
import {Scatter} from 'react-chartjs-2';

class TrendsChart extends React.Component {
  render() {
    console.log(this.props.chartData);
    return (
      <div>
        <Scatter data={this.props.recentTrendsChartData} redraw/>
      </div>
    );
  }
}

TrendsChart.defaultProps = {
};

export default TrendsChart;
