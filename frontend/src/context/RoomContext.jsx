import { createContext, useState, useEffect } from "react";
import { getUniqueValues } from "../pages/Room/RoomFilter";
import axios from "axios";

const RoomContext = createContext();

export default RoomContext


export const RoomProvider = ({ children }) => {
    const baseURL = "http://127.0.0.1:8000";
    const [rooms, setRooms] = useState([])
    const [sortedRooms, setRortedRooms] = useState([])
    const [featuredRooms, setFeaturedRooms] = useState([])
    const [checkedInRooms, setCheckedInRooms] = useState([])
    const [filteredCheckedInRooms, setfilteredCheckedInRooms] = useState([])

    const [loading, setLoding] = useState(true)
    const [reserved, setreserved] = useState(false)

    const [categoryName, setCategoryName] = useState('all')
    const [capacity, setCapacity] = useState('1')
    const [maxPrice, setmaxPrice] = useState(0)
    const [minPrice, setminPrice] = useState(0)
    const [maxRoomSize, setmaxRoomSize] = useState(0)
    const [minRoomSize, setminRoomSize] = useState(0)
    const [pricePerNight, setPricePerNight] = useState(0)


    useEffect(() => {
        async function fetchData() {
            try {
                const response = await axios.get(baseURL + "/hotel/api/v1/get_room_list/");
                const featured = response.data.filter((room) => room.featured);
                const minPrice = parseInt(Math.min(...getUniqueValues(response.data, "price_per_night")));
                const maxPrice = parseInt(Math.max(...getUniqueValues(response.data, "price_per_night")));
                const maxRoomSize = parseInt(Math.max(...getUniqueValues(response.data, "room_size")));
                const minRoomSize = parseInt(Math.min(...getUniqueValues(response.data, "room_size")));

                setRooms(response.data)
                setRortedRooms(response.data)
                setFeaturedRooms(featured)
                setmaxPrice(maxPrice)

                setminPrice(minPrice)

                setPricePerNight(maxPrice)


            } catch (error) {
                console.log(error);
            }
        }

        fetchData();
    }, []);

  
    const contextData = {
        rooms,
        setRooms,
        sortedRooms,
        setRortedRooms,
        categoryName,
        setCategoryName,
        reserved,
        setreserved,
        setmaxPrice,
        setminPrice,
        pricePerNight,
        setPricePerNight,
        maxPrice,
        minPrice,
    }

    return (
        <RoomContext.Provider value={contextData}>
            {children}
        </RoomContext.Provider>
    )

}