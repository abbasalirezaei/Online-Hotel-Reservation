import React, { useContext, useEffect, useState } from 'react'
import Slider from './Slider'
import Header from '../Header'
import { Link, useParams } from 'react-router-dom'
import useAxios from '../../utils/useAxios'
import RoomContext from '../../context/RoomContext.jsx'


export default function RoomDetail() {
    const { room_slug } = useParams()
    
    const { rooms } = useContext(RoomContext);

    const room = rooms.find(
        (room) => room.room_slug === room_slug
    );

    return (
        <div>
            
            <div >
                <section class="overflow-hidden bg-white py-11 font-poppins dark:bg-gray-800">
                    <div class="max-w-6xl px-4 py-4 mx-auto lg:py-8 md:px-6">


                        <div class="flex flex-wrap -mx-4">


                            <div class="w-full px-4 md:w-1/2 ">
                                <div class="sticky top-0 z-50 overflow-hidden ">
                                    <div class="relative mb-6 lg:mb-10 lg:h-2/4 ">
                                        <img src={room.cover_image} alt=""
                                            class="object-cover w-full lg:h-full " />
                                    </div>
                                    <div class="flex-wrap hidden md:flex ">
                                        <div class="w-1/2 p-2 sm:w-1/4">
                                            <a href="#"
                                                class="block border border-blue-300 dark:border-transparent dark:hover:border-blue-300 hover:border-blue-300">
                                                <img src="https://i.postimg.cc/PqYpFTfy/pexels-melvin-buezo-2529148.jpg" alt=""
                                                    class="object-cover w-full lg:h-20" />
                                            </a>
                                        </div>
                                        <div class="w-1/2 p-2 sm:w-1/4">
                                            <a href="#"
                                                class="block border border-transparent dark:border-transparent dark:hover:border-blue-300 hover:border-blue-300">
                                                <img src="https://i.postimg.cc/PqYpFTfy/pexels-melvin-buezo-2529148.jpg" alt=""
                                                    class="object-cover w-full lg:h-20" />
                                            </a>
                                        </div>
                                        <div class="w-1/2 p-2 sm:w-1/4">
                                            <a href="#"
                                                class="block border border-transparent dark:border-transparent dark:hover:border-blue-300 hover:border-blue-300">
                                                <img src="https://i.postimg.cc/PqYpFTfy/pexels-melvin-buezo-2529148.jpg" alt=""
                                                    class="object-cover w-full lg:h-20" />
                                            </a>
                                        </div>
                                        <div class="w-1/2 p-2 sm:w-1/4">
                                            <a href="#"
                                                class="block border border-transparent dark:border-transparent dark:hover:border-blue-300 hover:border-blue-300">
                                                <img src="https://i.postimg.cc/PqYpFTfy/pexels-melvin-buezo-2529148.jpg" alt=""
                                                    class="object-cover w-full lg:h-20" />
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>


                            <div class="w-full px-4 md:w-1/2 ">
                                <div class="lg:pl-20">
                                    <div class="mb-8 ">
                                       
                                        <h2 class="max-w-xl mt-2 mb-6 text-2xl font-bold dark:text-gray-400 md:text-4xl">
                                            {room.title}
                                        </h2>
                                       
                                        <p class="max-w-md mb-8 text-gray-700 dark:text-gray-400">
                                            {room.description}
                                        </p>
                                        <p class="inline-block mb-8 text-4xl font-bold text-gray-700 dark:text-gray-400 ">
                                            <span>${room.price_per_night}</span>
                                            <span
                                                class="text-base font-normal text-gray-500 line-through dark:text-gray-400">$1500.99</span>
                                        </p>
                                        <p class="text-green-600 dark:text-green-300 ">
                                            {room.is_booked ? (
                                                <p className="lead btn btn-danger btn-lg">Reserved</p>
                                            ) : (
                                                <p className="lead">

                                                    <Link
                                                        to={{
                                                            pathname: `/book/${room.room_slug}`,
                                                            state: { room },
                                                        }}
                                                        className="btn btn-primary btn-sm"
                                                        role="button"
                                                    >
                                                        Book Room
                                                    </Link>

                                                </p>
                                            )}
                                        </p>
                                    </div>
                                    
                                    
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        </div>
    )
}
