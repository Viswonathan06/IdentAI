import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import FileUpload from './components/FileUpload';
import 'bootstrap/dist/css/bootstrap.min.css';

// PrivateRoute component to handle authenticated routes
const PrivateRoute = ({ element: Element, ...rest }) => (
  <Route {...rest} element={(
    // Check if user is authenticated (you can implement your own authentication logic here)
    localStorage.getItem('isLoggedIn') === 'true'
      ? <Element />
      : <Navigate to="/" />
  )} />
);

function App() {
  // Check if user is authenticated
  const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Route for login page */}
          <Route exact path="/" element={<LoginPage />} />

          {/* Private route for dashboard */}
          {isLoggedIn ? (
            <Route path="/dashboard" element={<FileUpload />} />
          ) : (
            // Redirect to login page if not logged in
            <Route path="/" element={<Navigate to="/" />} />
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
