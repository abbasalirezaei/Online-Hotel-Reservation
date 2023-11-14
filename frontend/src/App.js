import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

// import { Nav } from './pages/Nav';

import Login from './components/Accounts/Login';

import RegisterPage from './components/Accounts/RegisterPage';
import Home from './pages/Home'
import { Nav } from './pages/Nav';
import RoomList from './pages/Room/RoomList';
import RoomDetail from './pages/Room/RoomDetail';
import ReservationForm from './pages/Room/ReservationForm';

import { AuthProvider } from './context/AuthContext';
import { RoomProvider } from './context/RoomContext';
import Dashboard from './components/Accounts/Dashboard';

function App() {
  return (
    <Router>
      <RoomProvider>
        <AuthProvider>
          <Nav />

          <Routes>
            <Route Component={Home} path="/" />
            <Route Component={Dashboard} path="/dashboard" />
            <Route Component={RoomList} path="/rooms" />
            <Route Component={RoomDetail} path="/room/:room_slug" />
            <Route
              path="/book/:room_slug"
              Component={ReservationForm}
            // render={(props) => <BookingPage {...props} />}
            />

            <Route Component={RegisterPage} path="/register" />

            <Route Component={Login} path='/login' />

            {/* <Route component={NotFound} path="*" exact /> */}

          </Routes>
        </AuthProvider>

      </RoomProvider>
    </Router>
  );
}

export default App;
