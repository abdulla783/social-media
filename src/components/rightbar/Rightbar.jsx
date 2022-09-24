import "./rightbar.css";
import { Users } from "../../dummyData";
import Online from "../online/Online";
import { useEffect, useState, useContext} from "react";
import axios from 'axios'
import {AuthContext} from '../../context/AuthContext'
import {Link} from "react-router-dom"
import { Add, Remove, Edit } from "@material-ui/icons";

export default function Rightbar({ user }) {
  const PF = process.env.REACT_APP_PUBLIC_FOLDER;
  const API_BE = process.env.REACT_APP_API_BE
  const [friends, setFriends] = useState([])
  const {user:currentUser, dispatch} = useContext(AuthContext)
  
  const [followed, setFollowed] = useState(currentUser?.following?.includes(user?.user?.id))

  const fetchFriends = async () => {
    let headers = {
      "Authorization": `Bearer ${currentUser?.access}`
    }
    const res = await axios.get(API_BE + `account/user-followings/${user?.user?.id ? user?.user?.id : currentUser.id }`, {headers: headers})
    if(res.status === 200){
      setFriends(res.data)
    } 
  }

  const handleClick = async() => {
    try{
      let headers = {
        "Authorization": `Bearer ${currentUser?.access}`
      }
      if(followed){
        axios.put(API_BE + `account/unfollow/${user?.user?.id}`, {}, {headers: headers})
        dispatch({type: "UNFOLLOW", payload: user?.user?.id})
      }else{
        axios.put(API_BE + `account/follow/${user?.user?.id}`, {}, {headers: headers})
        dispatch({type: "FOLLOW", payload: user?.user?.id})
      }

    }catch(err){

    }
    setFollowed(!followed)
  }

  useEffect(() =>{
    fetchFriends()
  }, [user?.user?.id])

  const HomeRightbar = () => {
    return (
      <>
        <div className="birthdayContainer">
          <img className="birthdayImg" src={PF + "gift.png"} alt="" />
          <span className="birthdayText">
            <b>Pola Foster</b> and <b>3 other friends</b> have a birhday today.
          </span>
        </div>
        <img className="rightbarAd" src={PF + "ad.png"} alt="" />
        <h4 className="rightbarTitle">Online Friends</h4>
        <ul className="rightbarFriendList">
          {Users.map((u) => (
            <Online key={u.id} user={u} />
          ))}
        </ul>
      </>
    );
  };

  const ProfileRightbar = () => {
    return (
      <>
       {user.user.id != currentUser.id && (
          <button className="rightbarFollowbutton" onClick={handleClick}>
            {followed ? "UnFollow": "Follow"}
            {followed ? <Remove /> : <Add />}
          </button>
        )}
        <h4 className="rightbarTitle">User information <Link style={{color: "black"}} to={`/profile/${user?.user?.id}/edit`} ><Edit /></Link></h4>
        <div className="rightbarInfo">
          <div className="rightbarInfoItem">
            <span className="rightbarInfoKey">City:</span>
            <span className="rightbarInfoValue">{user.city}</span>
          </div>
          <div className="rightbarInfoItem">
            <span className="rightbarInfoKey">From:</span>
            <span className="rightbarInfoValue">{user.country}</span>
          </div>
          <div className="rightbarInfoItem">
            <span className="rightbarInfoKey">Relationship:</span>
            <span className="rightbarInfoValue">{user.relationship}</span>
          </div>
        </div>
        <h4 className="rightbarTitle">User friends</h4>
        <div className="rightbarFollowings">
          {friends?.map((friend)=>(
            <Link style={{textDecoration: "none", color: "black"}} key={friend.id} to={`/profile/${friend?.id}`}>
              <div className="rightbarFollowing">
                <img
                  src={friend?.profile_image ? friend?.profile_image : PF + "Blank-Avatar.png"}
                  alt=""
                  className="rightbarFollowingImg"
                />
                <span className="rightbarFollowingName">{friend?.first_name} {friend?.last_name}</span>
              </div>
            </Link>
          ))}
        </div>
      </>
    );
  };
  return (
    <div className="rightbar">
      <div className="rightbarWrapper">
        {user ? <ProfileRightbar /> : <HomeRightbar />}
      </div>
    </div>
  );
}
