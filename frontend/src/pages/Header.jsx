import React from 'react'

export default function Header() {
    return (
        <div class=" bg-gray-200 flex items-center">
            <section class="w-full bg-cover bg-center py-32" style={{"backgroundImage": "url('https://source.unsplash.com/random')"}}>
                <div class="container mx-auto text-center text-white">
                    <h1 class="text-5xl font-medium mb-6">Welcome to My Agency</h1>
                    <p class="text-xl mb-12">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam viverra euismod odio,
                        gravida pellentesque urna varius vitae.</p>
                    <a href="#" class="bg-indigo-500 text-white py-4 px-12 rounded-full hover:bg-indigo-600">Demo</a>
                </div>
            </section>
        </div>

    )
}
