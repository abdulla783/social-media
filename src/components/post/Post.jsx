import "./post.css";
import { MoreVert } from "@material-ui/icons";
import { useState } from "react";
import {format} from "timeago.js"

import {Link} from "react-router-dom";
import axios from "axios";
import { useEffect, useContext } from "react";
import {AuthContext} from "../../context/AuthContext"

export default function Post({ post }) {
  const [like,setLike] = useState(post.likes.length)
  const [isLiked,setIsLiked] = useState(false)
  const PF = process.env.REACT_APP_PUBLIC_FOLDER;
  const API_BE = process.env.REACT_APP_API_BE

  const {user} = useContext(AuthContext)

  useEffect(()=>{
    setIsLiked(post.likes.includes(user?.id))
  }, [user?.id, post.likes])

  const likeHandler =()=>{
    try{
      const headers = {
        'Authorization': `Bearer ${user?.access}`
      }
      axios.put(API_BE + `post/like/${post?.id}`,{}, {headers: headers})
    }catch(err){}
    setLike(isLiked ? like-1 : like+1)
    setIsLiked(!isLiked)
  }
  return (
    <div className="post">
      <div className="postWrapper">
        <div className="postTop">
          <div className="postTopLeft">
            <Link to={`/profile/${post.user_id}`}>
              <img
                className="postProfileImg"
                src={post.profile_image !== '' ? post.profile_image : PF + 'Blank-Avatar.png'}
                alt=""
              />
            </Link>
            <span className="postUsername">
              {post.user}
            </span>
            <span className="postDate">{format(post.created_at)}</span>
          </div>
          <div className="postTopRight">
            <MoreVert />
          </div>
        </div>
        <div className="postCenter">
          <span className="postText">{post?.desc}</span>
          <img className="postImg" src={post.image} alt="" />
        </div>
        <div className="postBottom">
          <div className="postBottomLeft">
            <img className="likeIcon" src={PF + "like.png"} onClick={likeHandler} alt="" />
            <img className="likeIcon" src={PF + "heart.png"} onClick={likeHandler} alt="" />
            <span className="postLikeCounter">{like > 0 ? like : ""} people like it</span>
          </div>
          <div className="postBottomRight">
            <span className="postCommentText">{post?.comment} comments</span>
          </div>
        </div>
      </div>
    </div>
  );
}
