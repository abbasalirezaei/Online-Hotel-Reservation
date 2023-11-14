import React, { useContext, useEffect, useState } from 'react'
import RoomItem from './RoomItem'
import RoomFilter from './RoomFilter';
import RoomContext from '../../context/RoomContext';


export default function RoomList() {

    // async function fetchData() {
    //     try {
    //         const response = await axios.get(baseURL + "/hotel/api/v1/get_room_list/");
    //         const featured = response.data.filter((room) => room.featured);
    //         const minPrice = parseInt(Math.min(...getUniqueValues(response.data, "price_per_night")));
    //         const maxPrice = parseInt(Math.max(...getUniqueValues(response.data, "price_per_night")));
    //         const maxRoomSize = parseInt(Math.max(...getUniqueValues(response.data, "room_size")));
    //         const minRoomSize = parseInt(Math.min(...getUniqueValues(response.data, "room_size")));

    //         setRooms(response.data)
    //         setRortedRooms(response.data)
    //         setFeaturedRooms(featured)
    //         setmaxPrice(maxPrice)

    //         setminPrice(minPrice)

    //         setPricePerNight(maxPrice)


    //     } catch (error) {
    //         console.log(error);
    //     }
    // }
    // useEffect(() => {


    //     fetchData();
    // }, []);

    const { sortedRooms } = useContext(RoomContext)
    // const [rooms, setRooms] = useState([])

    return (
        <div >

            <section>
                <div className="mx-auto max-w-screen-xl px-4 py-8 sm:px-6 sm:py-12 lg:px-8">
                    <header>
                        <h2 className="text-xl font-bold text-gray-900 sm:text-3xl">
                            Rooms
                        </h2>

                    </header>



                    <div className="mt-4 lg:mt-8 lg:grid lg:grid-cols-4 lg:items-start lg:gap-8">
                        <RoomFilter />
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
            </section></div>
    )
}
