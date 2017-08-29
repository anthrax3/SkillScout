import React from 'react';
import {Scatter} from 'react-chartjs-2';
import cityTableData from '../../model/cityTableData.js';

let FilterableTable = require('react-filterable-table');

// Fields to show in the table, and what object properties in the data they bind to (city and state)
let fields = [
    { name: 'city', displayName: "City", inputFilterable: true, sortable: true },
    { name: 'state', displayName: "State", inputFilterable: true, sortable: true }
];

class CityList extends React.Component {
  render() {
    console.log(this.props.chartData);
    return (
      <FilterableTable
          namespace="Cities"
          initialSort="city"
          data={cityTableData}
          fields={fields}
          noRecordsMessage="No cities or states were found that match your search!"
          noFilteredRecordsMessage="No cities or states were found that match your filters!"
      />
    );
  }
}

CityList.defaultProps = {
};

export default CityList;
