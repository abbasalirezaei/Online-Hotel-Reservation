import React from 'react';

function Slider() {
	const image = "https://images.unsplash.com/photo-1625244724120-1fd1d34d00f6?auto=format&fit=crop&q=80&w=1000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aG90ZWxzfGVufDB8fDB8fHww"
   
	const images = [
		"https://images.unsplash.com/photo-1625244724120-1fd1d34d00f6?auto=format&fit=crop&q=80&w=1000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8aG90ZWxzfGVufDB8fDB8fHww"
   ,
		'https://source.unsplash.com/1600x900/?hotel',
		'https://source.unsplash.com/1600x900/?room',
		'https://source.unsplash.com/1600x900/?home',
		'https://source.unsplash.com/1600x900/?textures&patterns'
	];

	const [currentIndex, setCurrentIndex] = React.useState(1);

	const back = () => {
		if (currentIndex > 1) {
			setCurrentIndex(currentIndex - 1);
		}
	};

	const next = () => {
		if (currentIndex < images.length) {
			setCurrentIndex(currentIndex + 1);
		} else if (currentIndex <= images.length) {
			setCurrentIndex(images.length - currentIndex + 1);
		}
	};

	return (
		<div className="relative w-100 flex flex-shrink-0 overflow-hidden shadow-2xl" x-data="slider">
			<div className="rounded-full bg-gray-600 text-white absolute top-5 right-5 text-sm px-2 text-center z-10">
				<span x-text="currentIndex"></span>/
				<span x-text="images.length"></span>
			</div>

			{images.map((image, index) => (
				<figure key={index} className={`h-96 ${currentIndex === index + 1 ? 'visible' : 'hidden'}`}>
					<img src={image} alt="Image" className="absolute inset-0 z-10 h-full w-full object-cover opacity-70" />
					<figcaption className="absolute inset-x-0 bottom-1 z-20 w-96 mx-auto p-4 font-light text-sm text-center tracking-widest leading-snug bg-gray-300 bg-opacity-25">
						Any kind of content here!
						Primum in nostrane potestate est, quid meminerimus? Nulla erit controversia. Vestri haec verecundius, illi fortasse constantius.
					</figcaption>
				</figure>
			))}

			<button onClick={back} className="absolute left-14 top-1/2 -translate-y-1/2 w-11 h-11 flex justify-center items-center rounded-full shadow-md z-10 bg-gray-100 hover:bg-gray-200">
				<svg className="w-8 h-8 font-bold transition duration-500 ease-in-out transform motion-reduce:transform-none text-gray-500 hover:text-gray-600 hover:-translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
					xmlns="http://www.w3.org/2000/svg">
					<path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M15 19l-7-7 7-7">
					</path>
				</svg>
			</button>

			<button onClick={next} className="absolute right-14 top-1/2 translate-y-1/2 w-11 h-11 flex justify-center items-center rounded-full shadow-md z-10 bg-gray-100 hover:bg-gray-200">
				<svg className="w-8 h-8 font-bold transition duration-500 ease-in-out transform motion-reduce:transform-none text-gray-500 hover:text-gray-600 hover:translate-x-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"
					xmlns="http://www.w3.org/2000/svg">
					<path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M9 5l7 7-7 7"></path>
				</svg>
			</button>
		</div>
	);
}

export default Slider;
