import { useContext, useState } from "react";
import { Link } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import AuthContext from "../context/AuthContext";
export const Nav = () => {

    const { user, logoutUser } = useContext(AuthContext)
    const token = localStorage.getItem("authTokens")

    if (token) {
        const decoded = jwtDecode(token)
        var user_id = decoded.user_id
    }
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    return (
        <div className="navbar bg-gray-400">
            <div className="flex-1">
                <Link to="/" className="btn btn-ghost uppercase text-xl hover:">
                    My Hotel
                </Link>
            </div>
            <div className="navbar-start">
                <div className="dropdown">
                    <label tabIndex={0} className="btn btn-ghost lg:hidden">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h8m-8 6h16" /></svg>
                    </label>
                    <ul tabIndex={0} className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">
                        <li><Link to="/prodcuts" >محصولات</Link></li>
                        <li>
                            <a>Parent</a>
                            <ul className="p-2">
                                <li><a>Submenu 1</a></li>
                                <li><a>Submenu 2</a></li>
                            </ul>
                        </li>
                        <li><a>Item 3</a></li>
                    </ul>
                </div>
            </div>

            <div className="navbar-end">
                <Link className="btn btn-sm" to="/rooms">Rooms</Link>
            </div>
            <div className="flex-none">
                <div className="dropdown dropdown-end">
                    <label tabIndex={0} className="btn btn-ghost btn-circle">
                        <div className="indicator">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" /></svg>
                            <span className="badge badge-sm indicator-item">8</span>
                        </div>
                    </label>
                    <div tabIndex={0} className="mt-3 z-[1] card card-compact dropdown-content w-52 bg-base-100 shadow">
                        <div className="card-body">
                            <span className="font-bold text-lg">8 تا</span>
                            <span className="text-info">مجموع:
                                999 تومان
                            </span>
                            <div className="card-actions">
                                <button className="btn btn-primary btn-sm">مشاهده سبد خرید</button>
                            </div>
                        </div>
                    </div>
                </div>
                <button className="btn btn-ghost btn-circle">
                    <div className="indicator">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
                        <span className="badge badge-xs badge-primary indicator-item"></span>
                    </div>
                </button>

                <div className="dropdown dropdown-end ml-10">

                    <label tabIndex={0} className="btn btn-ghost btn-circle avatar">
                        <div className="w-10 rounded-full">
                            <img src="data:image/png;base64,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" />
                        </div>
                    </label>
                    <ul tabIndex={0} className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52">

                        {token === null ?
                            < >
                                <li>
                                    <Link to="/login" className="nav-link" >Login</Link>
                                </li>
                                <li>
                                    <Link to="/register" className="nav-link" >Register</Link>
                                </li>
                            </>
                            :
                            < >
                                <li>
                                    <a className="justify-between">
                                        Profile
                                        <span className="badge">New</span>
                                    </a>
                                </li>
                                <li><a>Settings</a></li>
                                <li><a onClick={logoutUser} >Logout</a></li>
                            </>

                        }


                    </ul>
                </div>

            </div>
        </div>
    );
};