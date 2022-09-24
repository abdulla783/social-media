import "./register.css";
import {useRef} from 'react'
import {useNavigate} from 'react-router-dom';
import axios from "axios";

const API_BE = process.env.REACT_APP_API_BE

export default function Register() {
  const username = useRef();
  const email = useRef();
  const password = useRef();
  const password2 = useRef();
  const history = useNavigate();

  const handleSubmit = async (e) => {
    e.prevenntDefault()

    if(password.current.value !== password2.current.value){
      password.current.setCustomValidity("Passwords don't match!");
    }else{
      const user = {
        username: username.current.value,
        email: email.current.value,
        password: password.current.value,
        password2: password2.current.value
      }
      try{
        const res = await axios.post(API_BE + "account/register", user);
        if(res.status === 201){
          history('/login')
        }
      }catch(err){
        console.log(err)
      }
    }

  }


  return (
    <div className="login">
      <div className="loginWrapper">
        <div className="loginLeft">
          <h3 className="loginLogo">Lamasocial</h3>
          <span className="loginDesc">
            Connect with friends and the world around you on Lamasocial.
          </span>
        </div>
        <div className="loginRight">
          <form className="loginBox" onSubmit={handleSubmit}>
            <input placeholder="Username" type="text" ref={username} className="loginInput" required />
            <input placeholder="Email" type="email" ref={email} className="loginInput" required />
            <input placeholder="Password" type="password" ref={password} className="loginInput" required />
            <input placeholder="Password Again" type="password" ref={password2} className="loginInput" required />
            <button className="loginButton" type="submit">Sign Up</button>
            <button className="loginRegisterButton">
              Log into Account
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
