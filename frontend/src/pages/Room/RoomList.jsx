import React, { useContext } from 'react'
import RoomItem from './RoomItem'
import RoomFilter from './RoomFilter';
import RoomContext from '../../context/RoomContext';

export default function RoomList() {
    const { sortedRooms } = useContext(RoomContext);

    return (
        <div dir="rtl" className="bg-[#f8fafc] min-h-screen py-10 px-2">
            <section>
                <div className="mx-auto max-w-7xl px-4 py-8 sm:px-8 sm:py-12">
                    <header className="mb-8 text-center">
                        <h2 className="text-3xl font-bold text-amber-700 mb-2">اتاق‌های ما</h2>
                        <p className="text-gray-500 text-base">انتخاب و رزرو بهترین اتاق متناسب با نیاز شما</p>
                    </header>
                    <div className="lg:grid lg:grid-cols-4 lg:gap-8 items-start">
                        <div className="mb-8 lg:mb-0">
                            <RoomFilter />
                        </div>
                        <div className="lg:col-span-3">
                            {sortedRooms && sortedRooms.length > 0 ? (
                                <ul className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
                                    {sortedRooms.map((room, index) => (
                                        <li key={index} className="rounded-2xl bg-white shadow-md hover:shadow-lg transition p-2">
                                            <RoomItem room={room} />
                                        </li>
                                    ))}
                                </ul>
                            ) : (
                                <div className="flex flex-col items-center justify-center h-64 text-gray-400">
                                    <svg className="w-16 h-16 mb-4" fill="none" stroke="currentColor" strokeWidth="1.5" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 17L9 21m5.25-4l.75 4m-7.5-4h10.5M12 3v10m0 0l-3.5-3.5M12 13l3.5-3.5" />
                                    </svg>
                                    <span>اتاقی برای نمایش وجود ندارد!</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </section>
        </div>
    )
}