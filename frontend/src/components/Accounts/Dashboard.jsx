import axios from 'axios'
import { jwtDecode } from 'jwt-decode'
import React, { useContext, useEffect, useState } from 'react'
import AuthContext from '../../context/AuthContext';
import useAxios from '../../utils/useAxios';
import RoomContext from '../../context/RoomContext';

export default function () {
    const baseURL = "http://127.0.0.1:8000";
    const token = localStorage.getItem("authTokens")

    const { setRooms, rooms, setRortedRooms, sortedRooms } = useContext(RoomContext);
    const [checkInRooms, setcheckInRooms] = useState([])
    const api = useAxios()

    if (token) {
        const decoded = jwtDecode(token)
        var user_id = decoded.user_id
        var is_staff = decoded.is_staff
    }

    useEffect(() => {
        setCheckedInRooms()
    }, []);

    const setCheckedInRooms = () => {

        if (is_staff) {
            api
                .get(
                    baseURL + "/hotel/api/v1/get_current_checked_in_rooms/"
                )
                .then((response) => {
                    setcheckInRooms(response.data);
                })
                .catch((error) => {
                    console.log(error.message);
                });
        }
    };

    const handleCheckOut = (room_id) => {

        // this.state.rooms.forEach((room) => {
        //     if (room.id === room_id) {
        //         room.is_booked = false;
        //     }
        // });
        // let updateCheckedInRooms = this.state.checkedInRooms.filter(
        //     (room) => room.room_id !== room_id
        // );
        // this.setState({
        //     checkedInRooms: updateCheckedInRooms,
        //     filteredCheckedInRooms: updateCheckedInRooms,
        // });

        api
            .post(baseURL + "/hotel/api/v1/checkout/", { pk: room_id })
            .then((response) => {
                const updatedRooms = rooms.map((item) => {
                    if (item.id === room_id) {
                        return {
                            ...item,
                            is_booked: false,
                        };
                    }
                    return item;
                });
        
        
                setRooms(updatedRooms);
        
                const updatedSortedRooms = sortedRooms.map((room) => {
                    if (room.id === room_id) {
                        return {
                            ...room,
                            is_booked: false,
                        };
                    }
                    return room;
                });
        
                setRortedRooms(updatedSortedRooms);


                let updateCheckedInRooms = checkInRooms.filter(
                    (room) => room.room_id !== room_id
                );
                // console.log(updateCheckedInRooms);
                setcheckInRooms(updateCheckedInRooms)


            })
            .catch((error) => {
                console.log(error.message);
            });
    };


    if (!token) {
        window.location.href = '/'
    }
    return (
        <div className='grid grid-rows-2'><div className="flex-col justify-center grid grid-rows-3">
            <div className="overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div className="inline-block min-w-full py-2 sm:px-6 lg:px-8">
                    <div className="overflow-hidden">
                        <table className="min-w-full text-left text-sm font-light">
                            <thead className="border-b font-medium dark:border-neutral-500">
                                <tr>
                                    <th scope="col" className="px-6 py-4">#</th>
                                    <th scope="col" className="px-6 py-4">Room</th>
                                    <th scope="col" className="px-6 py-4">Booked By</th>
                                    <th scope="col" className="px-6 py-4">Phone Number</th>
                                    <th scope="col" className="px-6 py-4">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                {
                                    checkInRooms.map((item, index) => {
                                        return (
                                            <tr key={index} className="border-b dark:border-neutral-500">
                                                <td className="whitespace-nowrap px-6 py-4 font-medium">{index + 1}</td>
                                                <td className="whitespace-nowrap px-6 py-4">{item.room_slug}</td>
                                                <td className="whitespace-nowrap px-6 py-4">{item.customer_name}</td>
                                                <td className="whitespace-nowrap px-6 py-4">{item.phone_number}</td>
                                                <td className="whitespace-nowrap px-6 py-4">

                                                    <button onClick={() => handleCheckOut(item.room_id)}
                                                        className="btn btn-outline-dark">Checkout</button>

                                                </td>
                                            </tr>
                                        )
                                    })
                                }



                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
        </div>
    )
}
