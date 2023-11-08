import React from 'react'
import Banner6 from './Banner6';
import Footer from './Footer';
import Newsletter from './Newsletter';
import ProductCard from './Room/ProductCard';
import { Link } from 'react-router-dom';

export default function Home() {
    const image1 = "https://www.seiu1000.org/sites/main/files/main-images/camera_lense_0.jpeg";
    const image2 = "https://buffer.com/library/content/images/2023/10/free-images.jpg";
    const image3 = "data:image/jpeg;base64,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"
    const image4 = "data:image/jpeg;base64,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";
    return (
        <div className='text-gray-400'>
            <div>
                <div className="container mx-auto p-5">

                    {/* Hero sectioin */}
                    <div className="md:flex md:flex-row mt-20">
                        <div className="md:w-2/5 flex flex-col justify-center items-center">
                            <h2 className="font-serif text-5xl text-gray-600 mb-4 text-center md:self-start md:text-left">
                                به سایت من خوش آمدی.
                            </h2>
                            <p className="uppercase text-gray-600 tracking-wide text-center md:self-start md:text-left">
                                فروشگاه عباس شاپ.
                            </p>
                            <p className="uppercase text-gray-600 tracking-wide text-center md:self-start md:text-left">
                                بهترین موبایل و تجیهزات گوشی را از ما بخرید.
                            </p>
                            <a
                                href="#"
                                className="bg-gradient-to-r from-red-600 to-pink-500 rounded-full py-4 px-8 text-gray-50 uppercase text-xl md:self-start my-5">
                                همین الان بخر
                            </a>
                        </div>
                        <div className="md:w-3/5">
                            <img src="https://ad2cart.com/wp-content/uploads/2021/02/ecommerce-website-banners.jpg"
                                className="w-full" />
                        </div>
                    </div>
                    {/* End Hero sectioin */}

                    <div className="my-20">
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

                            <ProductCard />
                            <ProductCard />
                            <ProductCard />
                            <ProductCard />
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
                            <ProductCard />
                            <ProductCard />
                            <ProductCard />
                            <ProductCard />
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
