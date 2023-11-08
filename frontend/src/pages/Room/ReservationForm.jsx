import React, { useEffect, useState } from 'react'
import axios from "axios";
import { Link, useParams } from "react-router-dom";
import { jwtDecode } from 'jwt-decode';
import useAxios from '../../utils/useAxios';

export default function ReservationForm() {
	const { room_slug } = useParams()
	const [room, setRoom] = useState({})
	const token = localStorage.getItem("authTokens")
	const api = useAxios()
	if (token) {
		const decode = jwtDecode(token)
		var user_id = decode.user_id

	}

	const [data, setData] = useState({
		email: "",
		phone_number: "",
		checking_date: "",
		checkout_date: "",
	});

	useEffect(() => {
		fetchRoom('/hotel/api/v1/get_a_room_detail/' + room_slug);

	}, []);

	const fetchRoom = (url) => {
		api.get(url)
			.then((response) => {
				setRoom(response.data);
			});
	}

	const handleSubmit = (event) => {
		event.preventDefault();

		let bookingDate = {
			email: data.email,
			phone_number: data.phone_number,
			checking_date: data.checking_date,
			checkout_date: data.checkout_date,
			room: room.id,
			customer: user_id,
		};
		
	
		api.post("/hotel/api/v1/book/", bookingDate, {
			headers: { "Content-Type": "application/json" },
		})
			.then(response => {
				console.log('Post created:', response.data);
				setData(
					{
						email: "",
						phone_number: "",
						checking_date: "",
						checkout_date: "",
					})
			})
			.catch(error => {
				console.error('Error creating post:', error);
			});
	};
	return (
		<div>
			<div classNameName='text-center mt-2'>
				< Link to={`/room/${room_slug}`} classNameName='btn justify-center text-center btn-sm bg-red-300'>Go to Room</Link>
			</div>
			<div className="flex items-center justify-center p-12">

				<div className="mx-auto w-full max-w-[550px]">
					<form action="https://formbold.com/s/FORM_ID" onSubmit={handleSubmit} >
						<div className="-mx-3 flex flex-wrap">
							<div className="w-full px-3 sm:w-1/2">
								<div className="mb-5">
									<label
										htmlFor="email"
										className="mb-3 block text-base font-medium text-[#07074D]"
									>
										Email
									</label>
									<input
										onChange={(event) => setData({ ...data, email: event.target.value })}
										type="email"

										name="email"
										id="email"
										placeholder="Email"
										className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
									/>


								</div>
							</div>

							<div className="w-full px-3 sm:w-1/2">
								<div className="mb-5">
									<label
										htmlFor="phone"
										className="mb-3 block text-base font-medium text-[#07074D]"
									>
										Phone Number
									</label>

									<input
										onChange={(event) =>
											setData({ ...data, phone_number: event.target.value })
										}
										type="text"
										name="phone"
										id="phone"
										placeholder="Phone Number"
										className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
									/>
								</div>
							</div>
						</div>
						<div classNameName="row" id="phoneID" style={{ display: "none" }}>
							<div classNameName="form-group col-md-6 m-auto text-danger">
								<p id="phone"></p>
							</div>
						</div>

						<div className="-mx-3 flex flex-wrap">
							<div className="w-full px-3 sm:w-1/2">
								<div className="mb-5">
									<label
										htmlFor="date"
										className="mb-3 block text-base font-medium text-[#07074D]"
									>
										Checking Date
									</label>


									<input
										onChange={(event) =>
											setData({ ...data, checking_date: event.target.value })
										}
										type="datetime-local"
										name="date"
										id="date"
										className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
									/>

								</div>
							</div>
							<div className="w-full px-3 sm:w-1/2">
								<div className="mb-5">
									<label
										htmlFor="checkout"
										className="mb-3 block text-base font-medium text-[#07074D]"
									>
										Checkout Date
									</label>
									<input
										onChange={(event) =>
											setData({ ...data, checkout_date: event.target.value })
										}
										type="datetime-local"
										name="time"
										id="checkout"
										className="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
									/>
								</div>
							</div>
						</div>

						<div classNameName="row" id="checkoutID" style={{ display: "none" }}>
							<div classNameName="form-group col-md-6 m-auto text-danger">
								<p id="checkout"></p>
							</div>
						</div>


						<div>
							<button
								type="submit"
								className="hover:shadow-form rounded-md bg-[#6A64F1] py-3 px-8 text-center text-base font-semibold text-white outline-none"
							>
								Submit
							</button>
						</div>
					</form>
				</div>
			</div></div>
	)
}
