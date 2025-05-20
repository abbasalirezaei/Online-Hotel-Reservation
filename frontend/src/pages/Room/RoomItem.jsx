import React from 'react'
import { Link } from 'react-router-dom'

export default function RoomItem({ room }) {
    const maxDescriptionLength = 60;
    const truncatedDescription =
        room.description.length > maxDescriptionLength
            ? `${room.description.substring(0, maxDescriptionLength)}...`
            : room.description;

    return (
        <div className="mx-auto">
            <article className="rounded-2xl bg-white shadow-lg hover:shadow-2xl transition-shadow duration-300 overflow-hidden border border-amber-100 group">
                <Link to={`/room/${room.room_slug}`} className="block focus:outline-none">
                    {/* تصویر اتاق */}
                    <div className="relative overflow-hidden h-56 rounded-b-2xl">
                        <img
                            src={room.cover_image}
                            alt={room.title}
                            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                        />
                        {/* امتیاز */}
                        <div className="absolute top-3 right-3 flex items-center rounded-full bg-white/90 px-3 py-1 shadow text-amber-700 text-sm font-bold">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-yellow-400 ml-1" viewBox="0 0 20 20" fill="currentColor">
                                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                            </svg>
                            4.9
                        </div>
                        {/* برچسب ویژه */}
                        {room.is_featured && (
                            <span className="absolute bottom-3 left-3 bg-amber-600 text-white text-xs px-3 py-1 rounded-full shadow">ویژه</span>
                        )}
                    </div>
                    {/* اطلاعات اتاق */}
                    <div className="p-4 text-right">
                        <h2 className="text-lg font-bold text-amber-900 mb-2 truncate">{room.title}</h2>
                        <p className="text-amber-700 text-sm mb-4 min-h-[40px]">{truncatedDescription}</p>
                        <div className="flex flex-row-reverse items-end justify-between">
                            <div>
                                <span className="text-xl font-extrabold text-amber-700">{room.price_per_night.toLocaleString()} </span>
                                <span className="text-amber-400 text-sm">تومان/هر شب</span>
                            </div>
                            <div className="group inline-flex rounded-xl bg-amber-100 p-2 hover:bg-amber-200 transition">
                                <svg xmlns="http://www.w3.org/2000/svg" className="group-hover:text-amber-600 h-5 w-5 text-amber-400" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M5 4a2 2 0 012-2h6a2 2 0 012 2v14l-5-2.5L5 18V4z" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </Link>
            </article>
        </div>
    )
}