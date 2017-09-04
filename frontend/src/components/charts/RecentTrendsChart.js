import React from 'react';
import {Line} from 'react-chartjs-2';

class TrendsChart extends React.Component {
  render() {
    console.log(this.props.recentTrendsChartData);
    return (
      <div>
        <Line data={this.props.recentTrendsChartData} redraw/>
      </div>
    );
  }
}

TrendsChart.defaultProps = {
};

export default TrendsChart;
