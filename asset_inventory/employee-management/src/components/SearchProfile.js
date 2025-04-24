import React, { useState } from 'react';
import axios from 'axios';

function SearchProfile() {
    const [employeeName, setEmployeeName] = useState('');
    const [profile, setProfile] = useState(null);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setEmployeeName(e.target.value);
    };

    const handleSearch = async (e) => {
        e.preventDefault();
        setError('');
        try {
            const response = await axios.get(`http://127.0.0.1:8000/search-profile/${employeeName}`);
            setProfile(response.data);
        } catch (err) {
            setError('Employee not found or error fetching data');
            setProfile(null);
        }
    };

    return (
        <div>
            {/* <h2>Search Employee Profile</h2> */}
            <form onSubmit={handleSearch}>
                <input
                    type="text"
                    value={employeeName}
                    onChange={handleChange}
                    placeholder="Enter employee name"
                    required
                />
                <button type="submit">Search</button>
            </form>
            {error && <p className="error">{error}</p>}
            {profile && (
                <div>
                    <h3>Profile Details:</h3>
                    <p>Employee Name: {profile.employee_name}</p>
                    <p>Laptop ID: {profile.laptop_id}</p>
                    <p>Adapter ID: {profile.adapter_id}</p>
                    <p>Charger ID: {profile.charger_id}</p>
                    <p>Mouse ID: {profile.mouse_id}</p>
                    <p>Date of Receiving: {profile.date_of_receiving}</p>
                    <p>Date of Returning: {profile.date_of_returning}</p>
                </div>
            )}
        </div>
    );
}

export default SearchProfile;
