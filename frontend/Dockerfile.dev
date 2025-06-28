FROM node:18-alpine

WORKDIR /app

# نصب پکیج‌های مورد نیاز
COPY package.json package-lock.json ./
RUN npm install

# تنظیم محیط برای hot-reloading
ENV WATCHPACK_POLLING=true
ENV CHOKIDAR_USEPOLLING=true

EXPOSE 3000

# استفاده از npm start برای اجرای برنامه در حالت توسعه با hot-reloading
CMD ["npm", "start"]