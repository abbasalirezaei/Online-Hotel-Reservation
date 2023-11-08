import React, { useContext } from "react";
import RoomContext from "../../context/RoomContext.jsx";



export const getUniqueValues = (rooms, type) => {
    return [...new Set(rooms?.map((room) => room[type]))];
};

export default function RoomFilter() {

    const { rooms,
        sortedRooms,
        setRortedRooms,
        categoryName,
        setCategoryName,
        reserved,
        setreserved,
        pricePerNight,
        setPricePerNight,
        maxPrice,
        minPrice

    } = useContext(RoomContext)


    let roomTypes = ["all", ...getUniqueValues(rooms, "category_name")];

    const selectTypes = roomTypes.map((cat, index) => (
        <option key={index} value={cat}>
            {cat}
        </option>
    ));




    const handleCategoryChange = (e) => {
       

        let filteredRooms = [...rooms]
        const category_name = e.target.value;
        setCategoryName(category_name)
        if (category_name !== "all") {
            filteredRooms = filteredRooms.filter(
                (room) => room.category_name === category_name
            );
        }

        // console.log(sortedRooms);
        // console.log(filteredRooms);


        setRortedRooms(filteredRooms)

    }

    const handleReservedChange = (e) => {
        setreserved(!reserved)

        let filteredRooms = [...rooms]

        if (!reserved) {
            filteredRooms = filteredRooms.filter((room) => room.is_booked === !reserved);
        }
        setRortedRooms(filteredRooms)
    }

    const handlePriceChange = (e) => {
        // console.log(e.target.value);
        let filteredRooms = [...rooms]
        setPricePerNight(e.target.value)
       
        filteredRooms = filteredRooms.filter(
            (room) => room.price_per_night <= parseInt(e.target.value)
        );
        // console.log(filteredRooms);
        setRortedRooms(filteredRooms)

    }
 


    const handelClear = () => {

        let filteredRooms = [...rooms]
        setRortedRooms(filteredRooms)
        setCategoryName("all")
        setreserved(false)
        setPricePerNight(maxPrice)

    }



    return (
        <>
            <form className="rooms-filter">
                <div className="form-group">
                    <label htmlFor="inputCategory">Category</label>
                    <select
                        id="inputCategory"
                        className="form-control"
                        name="categoryName"
                        value={categoryName}
                        onChange={handleCategoryChange}
                    >
                        {selectTypes}
                    </select>
                </div>

                {/* <div className="form-group">
          <label htmlFor="inputCapacity">Capacity</label>
          <select
            id="inputCapacity"
            className="form-control"
            name="capacity"
            value={capacity}
            onChange={handleChange}
          >
            {sleectCapacity}
          </select>
        </div> */}

                <div className="form-group">
                    <label htmlFor="customRange3">
                        Room Cost Max ${pricePerNight}
                    </label>
                    <input
                        name="price_per_night"
                        value={pricePerNight}
                        type="range"
                        className="custom-range pt-2"
                        min={minPrice}
                        max={maxPrice}
                        step="1.0"
                        id="customRange3"
                        onChange={handlePriceChange}
                    />
                </div>

                <div className="form-check pt-4">
                    <input
                        name="reserved"
                        checked={reserved}
                        type="checkbox"
                        className="form-check-input"
                        id="reserved"
                        onChange={handleReservedChange}
                    />
                    <label className="form-check-label" htmlFor="exampleCheck1">
                        Available
                    </label>
                </div>
                <button type="button" onClick={handelClear} className="btn-sm btn mt-4">clear</button>
                {/* <div className="border">Facility</div> */}
            </form>
        </>
    );
}
