import axios from "axios";
import { useEffect, useState } from "react";
import "./conversation.css";

export default function Conversation({ conversation, currentUser }) {
  const [user, setUser] = useState(null);
  const PF = process.env.REACT_APP_PUBLIC_FOLDER;
  const API_BE = process.env.REACT_APP_API_BE;

  useEffect(() => {
    const friendId = conversation.members.find((m) => m !== currentUser.id);

    const getUser = async () => {
      try {
        let headers = {
          "Authorization": `Bearer ${currentUser?.access}`
        }
        const res = await axios(API_BE + "account/user-profile/" + friendId, {headers:headers});
        setUser(res.data);
      } catch (err) {
        console.log(err);
      }
    };
    getUser();
  }, [currentUser, conversation]);

  return (
    <div className="conversation">
      <img
        className="conversationImg"
        src={
          user?.profile_image
            ? user?.profile_image
            : PF + "Blank-Avatar.png"
        }
        alt=""
      />
      <span className="conversationName">{user?.user?.username}</span>
    </div>
  );
}