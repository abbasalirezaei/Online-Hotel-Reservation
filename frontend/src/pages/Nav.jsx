import { useContext } from "react";
import { Link, NavLink } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import AuthContext from "../context/AuthContext";

export const Nav = () => {
    const { user, logoutUser } = useContext(AuthContext);
    const token = localStorage.getItem("authTokens");
    let user_id = null;
    if (token) {
        const decoded = jwtDecode(token);
        user_id = decoded.user_id;
    }

    return (
        <nav dir="rtl" className="fixed top-0 w-full z-50 bg-white shadow-md py-3 text-right">
            <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between">
                    {/* لوگو */}
                    <Link to="/" className="text-2xl font-bold tracking-tight text-amber-800 hover:text-blue-500 transition duration-300">
                        <span className="flex items-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 ml-2" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
                            </svg>
                            هتل خلیج فارس
                        </span>
                    </Link>

                    {/* منوی میانی */}
                    <div className="hidden md:flex items-center space-x-reverse space-x-8">
                        <Link to="/rooms" className="text-gray-700 font-medium hover:text-blue-500 transition duration-300 border-b-2 border-transparent hover:border-blue-500 pb-1">
                            اتاق ها
                        </Link>
                        <Link to="/products" className="text-gray-700 font-medium hover:text-blue-500 transition duration-300 border-b-2 border-transparent hover:border-blue-500 pb-1">
                            محصولات
                        </Link>
                        <Link to="/services" className="text-gray-700 font-medium hover:text-blue-500 transition duration-300 border-b-2 border-transparent hover:border-blue-500 pb-1">
                            خدمات
                        </Link>
                        <Link to="/about" className="text-gray-700 font-medium hover:text-blue-500 transition duration-300 border-b-2 border-transparent hover:border-blue-500 pb-1">
                            درباره ما
                        </Link>
                    </div>

                    {/* پروفایل */}
                    <div className="flex items-center gap-6">
                        {/* آیکون سبد خرید */}
                        <button className="relative group text-gray-600 hover:text-blue-500 transition duration-300">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                            </svg>
                            <span className="absolute -top-2 -left-2 bg-blue-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">
                                3
                            </span>
                        </button>

                        {token ? (
                            <div className="relative group">
                                <button className="w-10 h-10 rounded-full overflow-hidden border-2 border-blue-300 focus:outline-none hover:border-blue-500 transition duration-300 transform hover:scale-105">
                                    <img
                                        src="https://ui-avatars.com/api/?name=User&background=e6f2ff&color=3182ce"
                                        alt="profile"
                                        className="w-full h-full object-cover"
                                    />
                                </button>
                                <div className="absolute left-0 mt-2 w-48 bg-gray-20 rounded-lg shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform origin-top-left group-hover:translate-y-0 translate-y-2 z-20 text-right">
                                    <div className="py-3 px-4 border-b border-gray-100">
                                        <p className="text-sm font-medium text-gray-900">خوش آمدید</p>
                                        <p className="text-xs text-gray-500 mt-1">کاربر عزیز</p>
                                    </div>
                                    <div className="py-1">
                                        <Link to="/dashboard" className="flex items-center justify-end px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600">
                                            <span className="ml-2">داشبورد</span>
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                                            </svg>
                                        </Link>
                                        <Link to="/settings" className="flex items-center justify-end px-4 py-2 text-sm text-gray-700 hover:bg-blue-50 hover:text-blue-600">
                                            <span className="ml-2">تنظیمات</span>
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0..." />
                                            </svg>
                                        </Link>
                                    </div>
                                    <div className="py-1 border-t border-gray-100">
                                        <button onClick={logoutUser} className="flex w-full items-center justify-end px-4 py-2 text-sm text-red-600 hover:bg-red-50">
                                            <span className="ml-2">خروج</span>
                                            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                                            </svg>
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ) : (
                            <div className="flex items-center space-x-reverse space-x-3">
                                <Link to="/login" className="px-4 py-1 rounded-full font-medium text-blue-600 hover:text-blue-800 transition duration-300">
                                    ورود
                                </Link>
                                <Link to="/register" className="bg-blue-500 hover:bg-blue-600 text-white px-5 py-1.5 rounded-full font-medium transition duration-300 shadow-md hover:shadow-lg transform hover:scale-105">
                                    ثبت‌نام
                                </Link>
                            </div>
                        )}

                        {/* Mobile Menu Button */}
                        <button className="md:hidden text-gray-600 hover:text-blue-500">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16m-7 6h7" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Menu */}
            <div className="hidden md:hidden">
                <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 text-right">
                    <Link to="/rooms" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-500 hover:bg-gray-50">
                        اتاق‌ها
                    </Link>
                    <Link to="/products" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-500 hover:bg-gray-50">
                        محصولات
                    </Link>
                    <Link to="/services" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-500 hover:bg-gray-50">
                        خدمات
                    </Link>
                    <Link to="/about" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-500 hover:bg-gray-50">
                        درباره ما
                    </Link>
                </div>
            </div>
        </nav>
    );
};