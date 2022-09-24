import "./messanger.css"
import Topbar from "../../components/topbar/Topbar";
import Conversation from "../../components/conversations/Conversation";
import Message from "../../components/message/Message";
import ChatOnline from "../../components/chatOnline/ChatOnline";
import { useContext, useEffect, useCallback, useRef, useState } from "react";
// import { io } from "socket.io-client";
// import useWebSocket, { ReadyState } from 'react-use-websocket';
import { AuthContext } from "../../context/AuthContext";
import axios from "axios";

const API_BE = process.env.REACT_APP_API_BE;

export default function Messanger() {
    // const [socketUrl, setSocketUrl] = useState('ws://localhost:8000/');
    // const [messageHistory, setMessageHistory] = useState([]);

    const [conversations, setConversation] = useState([])
    const [messages, setMessages] = useState([])
    const [newMessage, setNewMessage] = useState("")
    const [currentChat, setCurrentChat] = useState(null)
    // const [socket, setSocket] = useState(null)
    const {user} = useContext(AuthContext)
    const scrollRef = useRef()

    // const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl, {
    //   onOpen: () => {
    //     console.log("Connected!")
    //   },
    //   onClose: () => {
    //     console.log("Disconnected!")
    //   }
    // });

    // useEffect(() => {
    //   if (lastMessage !== null) {
    //     setMessageHistory((prev) => prev.concat(lastMessage));
    //   }
    // }, [lastMessage, setMessageHistory]);
    // ${currentChat?.id}
    // const handleClickChangeSocketUrl = useCallback(
    //   () => setSocketUrl(`ws://127.0.0.1::8000/`),
    //   []
    // );
  
    // const handleClickSendMessage = useCallback(() => sendMessage('Hello'), []);
  
    // const connectionStatus = {
    //   [ReadyState.CONNECTING]: 'Connecting',
    //   [ReadyState.OPEN]: 'Open',
    //   [ReadyState.CLOSING]: 'Closing',
    //   [ReadyState.CLOSED]: 'Closed',
    //   [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    // }[readyState];

    const getConversation = async () =>{
        let headers = {
            "Authorization": `Bearer ${user?.access}`
        }
        const res = await axios.get(API_BE + 'conversation', {headers: headers})
        if(res.status === 200){
            setConversation(res.data)
        }
    }

    const getMessages = async () =>{
        let headers = {
            "Authorization": `Bearer ${user?.access}`
        }
        const res = await axios.get(API_BE + `conversation/messages?convo=${currentChat?.id}`, {headers: headers})
        if(res.status === 200){
            setMessages(res.data)
        }
    }

    useEffect(()=>{
        getConversation()
    }, [])

    useEffect(() =>{
        if(currentChat){
            setInterval(() => {
              getMessages()
            }, 3000);

        }
    }, [currentChat?.id])

    

    const handleSubmit = async(e) => {
        e.preventDefault()
        const message = {
            sender: user?.id,
            text: newMessage,
            conversation: currentChat?.id
        }
        try {
            let headers = {
                "Authorization": `Bearer ${user?.access}`
            }
            const res = await axios.post(API_BE + 'conversation/messages', message, {headers: headers})
            if(res.status === 201){
                setMessages([...messages, res.data])
                setNewMessage("")

            }
        } catch (error) {
            console.log(error)
        }
    }

    // window.setInterval(function() {
    //   console.log('ok')
    // }, 1000); 


    useEffect(()=>{
        scrollRef.current?.scrollIntoView({
            behavior: "smooth"
        })
    }, [messages])

    return (
        <>
          <Topbar />
          <div className="messenger">
            <div className="chatMenu">
              <div className="chatMenuWrapper">
                <input placeholder="Search for friends" className="chatMenuInput" />
                {conversations.map((c) => (
                  <div key={c?.id} onClick={() => setCurrentChat(c)}> 
                    <Conversation conversation={c} currentUser={user} />
                  </div>
                ))}
              </div>
            </div>
            <div className="chatBox">
              <div className="chatBoxWrapper">
                {currentChat ? (
                  <>
                    <div className="chatBoxTop">
                      {messages.map((m) => (
                        
                        <div key={m.id} ref={scrollRef}>
                          <Message message={m} own={m.sender === user.id} />
                        </div>
                      ))}
                    </div>
                    <div className="chatBoxBottom">
                      <textarea
                        className="chatMessageInput"
                        placeholder="write something..."
                        onChange={(e) => setNewMessage(e.target.value)}
                        value={newMessage}
                      ></textarea>
                      {/* <p>{connectionStatus}</p> */}
                      {/* <button
                        onClick={handleClickSendMessage}
                        disabled={readyState !== ReadyState.OPEN}
                      >
                        Click Me to send 'Hello'
                      </button> */}
                      <button className="chatSubmitButton" onClick={handleSubmit}>
                        Send
                      </button>
                    </div>
                  </>
                ) : (
                  <span className="noConversationText">
                    Open a conversation to start a chat.
                  </span>
                )}
              </div>
            </div>
            <div className="chatOnline">
              <div className="chatOnlineWrapper">
                {/* <ChatOnline
                  onlineUsers={onlineUsers}
                  currentId={user.id}
                  setCurrentChat={setCurrentChat}
                /> */}
              </div>
            </div>
          </div>
        </>
      );
}
