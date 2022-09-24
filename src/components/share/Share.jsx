import "./share.css";
import {PermMedia, Label,Room, EmojiEmotions, Cancel} from "@material-ui/icons"
import {AuthContext} from "../../context/AuthContext"
import { useContext, useRef, useState } from "react";
import axios from 'axios'

const PF = process.env.REACT_APP_PUBLIC_FOLDER;
const API_BE = process.env.REACT_APP_API_BE

export default function Share() {
  const { user } = useContext(AuthContext)
  const [file, setFile] = useState(null)
  const desc = useRef()

  const handleSubmit = async (e) => {
    e.preventDefault()
    let newPost = new FormData();
    newPost.append('desc', desc.current.value)
    newPost.append('user', user?.id)
    if(file !== null){
      newPost.append('image', file)
    }
   
    try {
      const res = await axios({
        method: "post",
        url: API_BE + "post/",
        data: newPost,
        headers: {"Authorization": `Bearer ${user?.access}`},})
      if(res.status === 201){
        setFile(null)
        desc.current.value = ""
        window.location.reload()
      }
    } catch (error) {
      console.log(error)
      window.location.reload()
    }
  }

  return (
    <div className="share">
      <div className="shareWrapper">
        <div className="shareTop">
          <img className="shareProfileImg" src={user?.profile_image ? user?.profile_image : PF + 'Blank-Avatar.png'} alt="" />
          <input
            placeholder={"What's in your mind " + user?.username + " ?"}
            className="shareInput"
            ref={desc}
          />
        </div>
        <hr className="shareHr"/>
        {file && (
          <div className="shareImageContainer">
            <img className="shareImg" src={URL.createObjectURL(file)} alt="" />
            <Cancel className="shareCancelImg" onClick={()=> setFile(null)} />
          </div>
        )}
        <form className="shareBottom" onSubmit={handleSubmit}>
            <div className="shareOptions">
                <label htmlFor="file" className="shareOption">
                    <PermMedia htmlColor="tomato" className="shareIcon"/>
                    <span className="shareOptionText">Photo or Video</span>
                    <input style={{display: "none"}} type="file" id="file" accept=".png, .jpeg, .jpg, .JPG, .PNG, .JPEG" onChange={(e)=>setFile(e.target.files[0])} />
                </label>
                <div className="shareOption">
                    <Label htmlColor="blue" className="shareIcon"/>
                    <span className="shareOptionText">Tag</span>
                </div>
                <div className="shareOption">
                    <Room htmlColor="green" className="shareIcon"/>
                    <span className="shareOptionText">Location</span>
                </div>
                <div className="shareOption">
                    <EmojiEmotions htmlColor="goldenrod" className="shareIcon"/>
                    <span className="shareOptionText">Feelings</span>
                </div>
            </div>
            <button className="shareButton" type="submit">Share</button>
        </form>
      </div>
    </div>
  );
}
