import "./login.css";
import { useRef, useContext } from "react"
import {Link} from "react-router-dom";
import { loginCall } from "../../apiCalls";
import {AuthContext} from "../../context/AuthContext"
import {CircularProgress} from "@material-ui/core"

export default function Login() {
  const username = useRef();
  const password = useRef();
  const {user, isFetching, error, dispatch} = useContext(AuthContext)

  const handleSubmit = (e) => {
    e.preventDefault();
    loginCall({ username: username.current.value, password: password.current.value }, dispatch)
  }


  return (
    <div className="login">
      <div className="loginWrapper">
        <div className="loginLeft">
          <h3 className="loginLogo">Saimsocial</h3>
          <span className="loginDesc">
            Connect with friends and the world around you on Lamasocial.
          </span>
        </div>
        <div className="loginRight">
          <form className="loginBox" onSubmit={handleSubmit}>
            <input placeholder="Username" type="text" className="loginInput" ref={username} required />
            <input placeholder="Password" type="password" className="loginInput" ref={password} required />
            <button disabled={isFetching} type="submit" className="loginButton">{isFetching ? <CircularProgress color="white" size="20px" /> : "Log In"}</button>
            <span className="loginForgot">Forgot Password?</span>
            {/* <Link to="/register"> */}
              <button disabled={isFetching} className="loginRegisterButton">
                Create a New Account
              </button>
            {/* </Link> */}
          </form>
        </div>
      </div>
    </div>
  );
}
