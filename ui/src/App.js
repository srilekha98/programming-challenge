import React, { useState, useEffect } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

function App() {
  const [data, setData] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortOrder, setSortOrder] = useState('asc');
  const [sortField, setSortField] = useState('id');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const response = await fetch('http://127.0.0.1:5000/movements');
    const jsonData = await response.json();
    setData(jsonData.response);
  };

  const handleSearchChange = (event) => {
    setSearchTerm(event.target.value);
  };

  const handleSort = (field) => {
    if (field === sortField) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('asc');
    }
  };

  const filteredData = data.filter((item) => {
    return item.origin_farm.toLowerCase().includes(searchTerm.toLowerCase());
  });

  const sortedData = filteredData.sort((a, b) => {
    const isAsc = sortOrder === 'asc';
    if (a[sortField] < b[sortField]) {
      return isAsc ? -1 : 1;
    }
    if (a[sortField] > b[sortField]) {
      return isAsc ? 1 : -1;
    }
    return 0;
  });

  return (
    <div>
      <input type="text" placeholder="Search" value={searchTerm} onChange={handleSearchChange} />
      <table>
        <thead>
          <tr>
            <th onClick={() => handleSort('origin_farm')}>origin farm </th>
            <th onClick={() => handleSort('dest_farm')}>dest farm </th>
            <th onClick={() => handleSort('num_units')}>number of units </th>
            <th onClick={() => handleSort('reason')}>reason</th>
          </tr>
        </thead>
        <tbody>
          {sortedData.map((item) => (
            <tr >
              <td>{item.origin_farm}</td>
              <td>{item.dest_farm}</td>
              <td>{item.num_units}</td>
              <td>{item.reason}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;