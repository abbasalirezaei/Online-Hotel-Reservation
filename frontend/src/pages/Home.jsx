import React, { useContext } from 'react'
import Banner6 from './Banner6';
import Footer from './Footer';
import Newsletter from './Newsletter';

import { Link } from 'react-router-dom';
import RoomContext from '../context/RoomContext';
import RoomItem from './Room/RoomItem';

export default function Home() {
    const { sortedRooms
    } = useContext(RoomContext
        )

    return (
        <div className='text-gray-400'>
            <div>
                <div className="container mx-auto p-5">

                    <div className="">
                        <div className="flex flex-row justify-between my-5">
                            <h2 className="text-3xl">Rooms</h2>
                            <Link to="/rooms" className="flex flex-row text-lg uppercase hover:text-gray-900  ">
                                View all rooms
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-5 ml-1" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                                        d="M14 5l7 7m0 0l-7 7m7-7H3"
                                    />
                                </svg>
                            </Link>
                        </div>

                        <div className="grid grid-flow-row grid-cols-1 md:grid-cols-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10">

                        {
                            sortedRooms ?

                                <div className="lg:col-span-3">
                                    <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

                                        {
                                            sortedRooms?.map((room, index) => {
                                                return <RoomItem key={index} room={room} />
                                            })
                                        }

                                    </ul>
                                </div> :
                                <h1>there is no room</h1>
                        }
                        </div>
                    </div>

                    {/* End Men's Collection Section */}

                    {/* Banner */}
                    <Banner6 />
                    {/* end banner */}
                    <div className="my-10">
                        <div className="flex flex-row justify-between my-5">
                            <h2 className="text-3xl">Rooms</h2>
                            <a href="#" className="flex flex-row text-lg uppercase hover:text-gray-900  ">
                               View All
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-5 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                                </svg>
                            </a>
                        </div>
                        <div className="grid grid-flow-row grid-cols-1 md:grid-cols-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10">
                        {
                            sortedRooms ?

                                <div className="lg:col-span-3">
                                    <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

                                        {
                                            sortedRooms?.map((room, index) => {
                                                return <RoomItem key={index} room={room} />
                                            })
                                        }

                                    </ul>
                                </div> :
                                <h1>there is no room</h1>
                        }
                        </div>
                    </div>

                    {/* End Women's Collection Section */}



                    {/* Newsletter Section */}
                    <Newsletter />

                    {/* End Newsletter Section */}


                    {/* Footer Section */}
                    <Footer />
                    {/* End Footer Section */}
                </div>

            </div>
        </div>
    )
}
