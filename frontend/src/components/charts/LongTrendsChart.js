import React from 'react';
import {Line} from 'react-chartjs-2';

class TrendsChart extends React.Component {
  render() {
    console.log(this.props.chartData);
    return (
      <div>
        <Line data={this.props.longTrendsChartData} redraw/>
      </div>
    );
  }
}

TrendsChart.defaultProps = {
};

export default TrendsChart;
