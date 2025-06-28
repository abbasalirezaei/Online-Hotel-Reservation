import React, { useContext, useState, useEffect } from 'react';
import { Link, useParams } from 'react-router-dom';
import RoomContext from '../../context/RoomContext.jsx';

export default function RoomDetail() {
    const { room_slug } = useParams();
    const { rooms, roomImages } = useContext(RoomContext);
    const room = rooms?.find((r) => r.room_slug === room_slug);

    const images = room && roomImages
        ? roomImages.filter((img) => img.room === room.id)
        : [];

    const [mainImage, setMainImage] = useState(room?.cover_image);
    useEffect(() => {
        setMainImage(room?.cover_image);
    }, [room?.cover_image]);

    const formatPrice = (price) =>
        price ? Number(price).toLocaleString() + ' تومان' : '-';

    if (!room) return <div className="text-center py-10 text-gray-500">اتاق پیدا نشد</div>;

    return (
        <div dir="rtl" className="bg-white text-gray-800 min-h-screen py-10 px-6">
            <div className="max-w-4xl mx-auto space-y-10">

                {/* Title & Price */}
                <div className="space-y-4 border-b pb-6">
                    <h1 className="text-3xl font-bold">{room.title}</h1>
                    <div className="text-xl text-amber-700 font-semibold">
                        {formatPrice(room.price_per_night)}
                        {room.discount_price && (
                            <span className="text-red-500 text-base mx-3 line-through">
                                {formatPrice(room.discount_price)}
                            </span>
                        )}
                    </div>
                    <div className="text-sm text-gray-500">
                        <span>کد اتاق: {room.room_code || '-'}</span> |{' '}
                        <span>دسته‌بندی: {room.category_name}</span>
                    </div>
                </div>

                {/* Room Quick Info */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-sm text-gray-700">
                    <div>ظرفیت: <b>{room.capacity}</b></div>
                    <div>تعداد تخت: <b>{room.bed_count}</b></div>
                    <div>نوع تخت: <b>
                        {room.bed_type === 'single' ? 'تک نفره' :
                            room.bed_type === 'double' ? 'دو نفره' :
                                room.bed_type === 'king' ? 'کینگ' : 'دوتخته جدا'}
                    </b></div>
                    <div>طبقه: <b>{room.floor}</b></div>
                    <div>اندازه: <b>{room.room_size}</b></div>
                    <div>امتیاز: <b>{room.rating} ⭐</b></div>
                    <div>بازدید: <b>{room.views}</b></div>
                    <div>وضعیت: <b className={room.active ? "text-green-600" : "text-red-500"}>{room.active ? "فعال" : "غیرفعال"}</b></div>
                    <div>حیوان خانگی: <b>{room.pets ? "مجاز" : "مجاز نیست"}</b></div>
                    <div>صبحانه: <b>{room.breakfast ? "دارد" : "ندارد"}</b></div>
                </div>

                {/* Images */}
                <div className="space-y-4">
                    <img
                        src={mainImage}
                        alt="Main room"
                        className="w-full h-72 object-cover rounded-xl border"
                    />
                    <div className="flex gap-2 flex-wrap">
                        {[room.cover_image, ...images.map(img => img.display_images)].map((imgSrc, idx) => (
                            <img
                                key={idx}
                                src={imgSrc}
                                onClick={() => setMainImage(imgSrc)}
                                className={`w-20 h-16 rounded-lg object-cover cursor-pointer border-2 transition-all duration-200
                                    ${mainImage === imgSrc ? 'border-amber-600' : 'border-gray-200'}`}
                                alt={`room-thumb-${idx}`}
                            />
                        ))}
                    </div>
                </div>

                {/* Description & Amenities */}
                <div className="space-y-6 text-sm leading-6">
                    <div>
                        <h2 className="font-bold text-lg mb-2">توضیحات</h2>
                        <p className="text-gray-600">{room.description}</p>
                    </div>
                    {room.amenities?.length > 0 && (
                        <div>
                            <h2 className="font-bold text-lg mb-2">امکانات</h2>
                            <ul className="list-disc pr-5 text-gray-700">
                                {room.amenities.map((item, idx) => (
                                    <li key={idx}>{item}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>

                {/* Reservation */}
                <div className="pt-6 border-t">
                    {room.is_booked ? (
                        <div className="px-4 py-2 bg-red-100 text-red-600 rounded-lg text-center font-semibold">رزرو شده</div>
                    ) : (
                        <Link
                            to={`/book/${room.room_slug}`}
                            className="block text-center px-4 py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg font-semibold"
                        >
                            رزرو اتاق
                        </Link>
                    )}
                </div>

                {/* Dates */}
                <div className="text-xs text-gray-400 text-center mt-8">
                    <span>ایجاد: {new Date(room.created_at).toLocaleDateString('fa-IR')}</span> |{' '}
                    <span>ویرایش: {new Date(room.updated_at).toLocaleDateString('fa-IR')}</span>
                </div>
            </div>
        </div>
    );
}
