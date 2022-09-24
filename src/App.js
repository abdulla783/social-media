import Home from "./pages/home/Home";
import Login from "./pages/login/Login";
import Profile from "./pages/profile/Profile";
import Register from "./pages/register/Register";
import Messanger from "./pages/messanger/Messanger";
import Editprofile from "./pages/profile/Editprofile";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import {useContext} from "react"
import {AuthContext} from "./context/AuthContext"

function App() {
  const {user} = useContext(AuthContext)
  return (
    <Router>
      <Routes>
        <Route path="/" element={user? <Home/> : <Login />} />
        <Route path="/login" element={user ? <Navigate to="/" /> : <Login/>} />
        <Route path="/register" element={user ? <Navigate to="/" /> : <Register/>} />
        <Route path="/profile/:id" element={user ? <Profile/> : <Login/>} />
        <Route path="/profile/:id/edit" element={user ? <Editprofile/> : <Login/>} />
        <Route path="/messanger" element={!user ? <Navigate to="/" /> : <Messanger />} />
      </Routes>
    </Router>
  )
}

export default App;
