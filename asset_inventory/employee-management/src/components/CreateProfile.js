import React, { useState } from 'react';
import axios from 'axios';

function CreateProfile() {
    const [profile, setProfile] = useState({
        employee_name: '',
        laptop_id: '',
        adapter_id: '',
        charger_id: '',
        mouse_id: '',
        date_of_receiving: '',
        date_of_returning: ''
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProfile({ ...profile, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Make a POST request to your FastAPI backend
            const response = await axios.post('http://127.0.0.1:8000/create-profile/', profile);
            console.log('Profile created:', response.data);
            alert('Profile created successfully');
        } catch (error) {
            console.error('Error creating profile:', error);
            alert('Error creating profile');
        }
    };

    return (
        <div>
            {/* <h2>Create Employee Profile</h2> */}
            <form onSubmit={handleSubmit}>
                <input
                    type="text"
                    name="employee_name"
                    value={profile.employee_name}
                    onChange={handleChange}
                    placeholder="Employee Name"
                    required
                />
                <input
                    type="text"
                    name="laptop_id"
                    value={profile.laptop_id}
                    onChange={handleChange}
                    placeholder="Laptop ID"
                    required
                />
                <input
                    type="text"
                    name="adapter_id"
                    value={profile.adapter_id}
                    onChange={handleChange}
                    placeholder="Adapter ID"
                    required
                />
                <input
                    type="text"
                    name="charger_id"
                    value={profile.charger_id}
                    onChange={handleChange}
                    placeholder="Charger ID"
                    required
                />
                <input
                    type="text"
                    name="mouse_id"
                    value={profile.mouse_id}
                    onChange={handleChange}
                    placeholder="Mouse ID"
                    required
                />
                <input
                    type="date"
                    name="date_of_receiving"
                    value={profile.date_of_receiving}
                    onChange={handleChange}
                    required
                />
                <input
                    type="date"
                    name="date_of_returning"
                    value={profile.date_of_returning}
                    onChange={handleChange}
                    required
                />
                <button type="submit">Create Profile</button>
            </form>
        </div>
    );
}

export default CreateProfile;
