import React, { useContext, useState } from 'react';
import AuthContext from '../../context/AuthContext';
import { jwtDecode } from 'jwt-decode';

function RegisterPage() {
    const token = localStorage.getItem("authTokens")

    if (token) {
        const decoded = jwtDecode(token)
        var user_id = decoded.user_id
    }

    const [email, setEmail] = useState("")
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const [password2, setPassword2] = useState("")

    const { registerUser } = useContext(AuthContext)

    const handelSubmit = async (e) => {
        // if you dont and add this, your page after submit will be refreshed
        e.preventDefault()
        // we need email and password from the form.
        // this is like request.Post.get("email")

        registerUser(email, username, password, password2)
    }
    if (token) {
        window.location.href = '/'
    }
    else {
        return (
            <div className="flex flex-col h-screen bg-gray-100">
                <div className="grid place-items-center mx-2 my-20 sm:my-auto">


                    <div className="w-11/12 p-12 sm:w-8/12 md:w-6/12 lg:w-5/12 2xl:w-4/12 
            px-6 py-10 sm:px-10 sm:py-6 
            bg-white rounded-lg shadow-md lg:shadow-lg">
                        <h2 className="text-center font-semibold text-3xl lg:text-4xl text-gray-800">
                            Register
                        </h2>
                        <form className="mt-10" method="POST" onSubmit={handelSubmit}>
                            <label htmlFor="email" className="block text-xs font-semibold text-gray-600 uppercase">E-mail</label>
                            <input
                                id="email"
                                type="email"
                                name="email"
                                onChange={e => setEmail(e.target.value)}
                                placeholder="e-mail address"
                                autoComplete="email"
                                className="block w-full py-3 px-1 mt-2 
              text-gray-800 appearance-none 
              border-b-2 border-gray-100
              focus:text-gray-500 focus:outline-none focus:border-gray-200"
                                required
                            />
                            <label htmlFor="register" className="block text-xs font-semibold text-gray-600 uppercase">UserName</label>
                            <input
                                id="register"
                                type="text"
                                onChange={e => setUsername(e.target.value)}
                                name="email"
                                placeholder="Enter your username"
                                autoComplete="email"
                                className="block w-full py-3 px-1 mt-2 
              text-gray-800 appearance-none 
              border-b-2 border-gray-100
              focus:text-gray-500 focus:outline-none focus:border-gray-200"
                                required
                            />

                            <label htmlFor="password" className="block mt-2 text-xs font-semibold text-gray-600 uppercase">Password</label>
                            <input
                                id="password"
                                type="password"
                                name="password"
                                placeholder="password"
                                onChange={e => setPassword(e.target.value)}
                                autoComplete="current-password"
                                className="block w-full py-3 px-1 mt-2 mb-4
              text-gray-800 appearance-none 
              border-b-2 border-gray-100
              focus:text-gray-500 focus:outline-none focus:border-gray-200"
                                required
                            />


                            <label htmlFor="password2" className="block mt-2 text-xs font-semibold text-gray-600 uppercase">Password2</label>
                            <input
                                id="password2"
                                type="password"
                                name="password"
                                onChange={e => setPassword2(e.target.value)}
                                placeholder="password"
                                autoComplete="current-password"
                                className="block w-full py-3 px-1 mt-2 mb-4
              text-gray-800 appearance-none 
              border-b-2 border-gray-100
              focus:text-gray-500 focus:outline-none focus:border-gray-200"
                                required
                            />

                            <button
                                type="submit"
                                className="w-full py-3 mt-10 bg-gray-800 rounded-sm
              font-medium text-white uppercase
              focus:outline-none hover:bg-gray-700 hover:shadow-none"
                            >
                                Register
                            </button>
                            <div className="sm:flex sm:flex-wrap mt-8 sm:mb-4 text-sm text-center">
                                <a href="#" className="flex-2 underline">
                                    Forgot password?
                                </a>
                                <p className="flex-1 text-gray-500 text-md mx-4 my-1 sm:my-auto">
                                    or
                                </p>
                                <a href="#" className="flex-2 underline">
                                    Create an Account
                                </a>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
}

export default RegisterPage;
