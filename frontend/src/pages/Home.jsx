import React, { useContext } from 'react'
import Footer from './Footer';
import Newsletter from './Newsletter';
import { Link } from 'react-router-dom';
import RoomContext from '../context/RoomContext';
import RoomItem from './Room/RoomItem';

export default function Home() {
    const { sortedRooms } = useContext(RoomContext);

    return (
        <div className="bg-amber-50 min-h-screen rtl text-right">
            {/* Hero Banner */}
            <div className="relative h-96 bg-amber-800 overflow-hidden">
                <div 
                    className="absolute inset-0 bg-cover bg-center opacity-40"
                    style={{ backgroundImage: "url('/hotel-image.jpg')" }}
                ></div>
                <div className="container mx-auto px-5 h-full flex flex-col justify-center items-end">
                    <h1 className="text-5xl md:text-6xl font-light text-white mb-4">آرامش خانه دوم شما</h1>
                    <p className="text-xl text-white max-w-md mb-8">اقامتی دلنشین با امکانات مدرن و کیفیت استثنایی</p>
                    {/* <Link to="/rooms" className="bg-white text-amber-800 px-8 py-3 rounded-sm hover:bg-amber-100 transition duration-300 w-max">
                        مشاهده اتاق‌ها
                    </Link> */}
                </div>
            </div>
            
            {/* Main Content */}
            <div className="container mx-auto px-5 py-16">
                {/* Featured Rooms Section */}
                <div className="mb-20">
                    <div className="flex flex-row-reverse justify-between items-center mb-10">
                        <h2 className="text-3xl font-light text-amber-900">اتاق‌های ویژه</h2>
                        <Link to="/rooms" className="flex flex-row-reverse items-center text-amber-800 hover:text-amber-900 transition">
                            <span className="ml-2">مشاهده همه</span>
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                            </svg>
                        </Link>
                    </div>

                    {sortedRooms ? (
                        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
                            {sortedRooms.slice(0, 3).map((room, index) => (
                                <RoomItem key={index} room={room} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-16 text-amber-800">
                            <p className="text-xl">در حال حاضر اتاقی برای نمایش وجود ندارد</p>
                        </div>
                    )}
                </div>

                {/* Amenities Section */}
                <div className="mb-20 py-16 bg-amber-100 -mx-5 px-5">
                    <h2 className="text-3xl font-light text-amber-900 mb-12 text-center">امکانات و خدمات</h2>
                    <div className="grid gap-8 md:grid-cols-3">
                        <div className="flex flex-col items-center text-center">
                            <div className="w-16 h-16 flex items-center justify-center rounded-full bg-amber-200 mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-amber-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                            <h3 className="text-xl text-amber-900 mb-2">اینترنت پرسرعت</h3>
                            <p className="text-amber-700">دسترسی به اینترنت وای‌فای پرسرعت در تمام فضای اقامتگاه</p>
                        </div>
                        <div className="flex flex-col items-center text-center">
                            <div className="w-16 h-16 flex items-center justify-center rounded-full bg-amber-200 mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-amber-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                                </svg>
                            </div>
                            <h3 className="text-xl text-amber-900 mb-2">صبحانه رایگان</h3>
                            <p className="text-amber-700">صبحانه بوفه با تنوع غذایی بالا برای آغاز روزی پرانرژی</p>
                        </div>
                        <div className="flex flex-col items-center text-center">
                            <div className="w-16 h-16 flex items-center justify-center rounded-full bg-amber-200 mb-4">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-amber-800" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                                </svg>
                            </div>
                            <h3 className="text-xl text-amber-900 mb-2">خدمات نظافت</h3>
                            <p className="text-amber-700">نظافت روزانه اتاق‌ها با رعایت استانداردهای بهداشتی</p>
                        </div>
                    </div>
                </div>

                {/* Popular Rooms Section */}
                <div className="mb-20">
                    <div className="flex flex-row-reverse justify-between items-center mb-10">
                        <h2 className="text-3xl font-light text-amber-900">محبوب‌ترین اتاق‌ها</h2>
                        <Link to="/rooms" className="flex flex-row-reverse items-center text-amber-800 hover:text-amber-900 transition">
                            <span className="ml-2">مشاهده همه</span>
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                            </svg>
                        </Link>
                    </div>

                    {sortedRooms ? (
                        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
                            {sortedRooms.slice(0, 3).map((room, index) => (
                                <RoomItem key={index} room={room} />
                            ))}
                        </div>
                    ) : (
                        <div className="text-center py-16 text-amber-800">
                            <p className="text-xl">در حال حاضر اتاقی برای نمایش وجود ندارد</p>
                        </div>
                    )}
                </div>

                {/* Newsletter Section */}
                <div className="bg-amber-100 -mx-5 px-5 py-16">
                    <Newsletter />
                </div>
            </div>

            {/* Footer */}
            <Footer />
        </div>
    )
}