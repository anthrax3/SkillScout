import React from 'react';
import {Doughnut} from 'react-chartjs-2';

class DoughnutChart extends React.Component {
  render() {
    console.log(this.props.chartData);
    return (
      <div>
        <Doughnut data={this.props.doughnutChartData} redraw/>
      </div>
    );
  }
}

DoughnutChart.defaultProps = {
};

export default DoughnutChart;
