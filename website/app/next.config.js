/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        'MYSQL_HOST': '127.0.0.1',
        'MYSQL_PORT': '3306',
        'MYSQL_DATABASE': 'csce483',
        'MYSQL_USER': 'rpi',
        'MYSQL_PASSWORD': 'Hogr!ders483',
    }
}

module.exports = nextConfig
