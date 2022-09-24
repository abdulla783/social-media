import React from 'react'
import "../../components/rightbar/rightbar.css"
import "./editProfile.css"
import Topbar from '../../components/topbar/Topbar'
import Sidebar from '../../components/sidebar/Sidebar'
import EditProfileForm from '../../components/profile/EditProfileForm'
import Rightbar from '../../components/rightbar/Rightbar'
import { useParams } from 'react-router-dom';

export default function Editprofile() {
    const PF = process.env.REACT_APP_PUBLIC_FOLDER;
    const API_BE = process.env.REACT_APP_API_BE
    const { id } = useParams()

    return (
        <>
            <Topbar />
            <div className="homeContainer">
                <Sidebar />
                <EditProfileForm />
                <Rightbar />
            </div>
        </>
    )
}
