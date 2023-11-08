import React from 'react'

export default function Newsletter() {
    const image = "https://th.bing.com/th/id/R.1395d1b17397018e6916784c283a14f2?rik=bmfmSW7odc2D1A&pid=ImgRaw&r=0"
    return (
        <div className="relative mx-auto my-5 max-w-4xl rounded-lg bg-indigo-100 shadow-lg">
            <svg xmlns="http://www.w3.org/2000/svg" className="absolute right-2 top-2 h-6 w-6 cursor-pointer" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
            <div className="p-8 md:p-12 lg:px-16">
                <div className="max-w-lg">
                    <h2 className="text-2xl font-bold text-indigo-900 md:text-3xl">Subscribe to stay ahead</h2>
                    <p className="hidden text-indigo-900 sm:mt-4 sm:block">Lorem ipsum dolor sit amet consectetur adipisicing elit. Facere temporibus dicta mollitia!</p>
                </div>
                <div className="mt-8 max-w-xl">
                    <form action="#" className="sm:flex sm:gap-4">
                        <div className="sm:flex-1">
                            <label htmlFor="email" className="sr-only">Email</label>
                            <input type="email" placeholder="Email address" className="w-full rounded-md border-indigo-200 bg-white p-3 text-indigo-700 shadow-sm transition focus:border-white focus:outline-none focus:ring focus:ring-indigo-400" />
                        </div>
                        <button type="submit" className="group mt-4 flex w-full items-center justify-center rounded-md bg-indigo-600 px-5 py-3 text-white transition focus:outline-none focus:ring focus:ring-indigo-400 sm:mt-0 sm:w-auto">
                            <span className="text-sm font-medium"> Sign Up </span>
                            <svg className="ml-3 h-5 w-5 transition-all group-hover:translate-x-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                            </svg>
                        </button>
                    </form>
                </div>
            </div>
        </div>

    )
}
