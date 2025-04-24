import React from 'react';
import CreateProfile from './components/CreateProfile'; // Import the CreateProfile component
import SearchProfile from './components/SearchProfile'; // Import the SearchProfile component
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Employee Management System</h1> {/* Custom header */}
      </header>
      <main>
        <section>
          <h2>Create Employee Profile</h2>
          <CreateProfile />  {/* Render the CreateProfile component */}
        </section>
        <section>
          <h2>Search Employee Profile</h2>
          <SearchProfile />  {/* Render the SearchProfile component */}
        </section>
      </main>
    </div>
  );
}

export default App;
