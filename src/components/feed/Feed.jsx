import Post from "../post/Post";
import Share from "../share/Share";
import "./feed.css";
import React, {useState, useEffect} from "react";
import axios from "axios";
import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

const API_BE = process.env.REACT_APP_API_BE

export default function Feed({user_id}) {
  const [posts, setPosts] = useState([])
  const {user} = useContext(AuthContext)

  console.log(user_id,'==id==', user?.id)
  const fetchPosts = async () => {
    const headers = {
      'Authorization': `Bearer ${user?.access}`
    }
    const res = user_id !== undefined 
    ?  await axios.get(API_BE + `post/myposts/${user_id}`, {headers: headers})
    : await axios.get(API_BE + "post/timeline", {headers: headers})
    if(res.status === 200) {
      console.log(res.data)
      setPosts(res.data)
    }
  }

  useEffect(() => {
    fetchPosts()
  }, [user_id])

  return (
    <div className="feed">
      <div className="feedWrapper">
        {user_id == user?.id && <Share />}
        {user_id == undefined && <Share />}
        {posts.map((p) => (
          <Post key={p.id} post={p} />
        ))}
      </div>
    </div>
  );
}
