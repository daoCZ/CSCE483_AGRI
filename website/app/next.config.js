/** @type {import('next').NextConfig} */
const nextConfig = {
    env: {
        'MYSQL_HOST': 'hogrider-mysql.mysql.database.azure.com',
        'MYSQL_DATABASE': 'csce483',
        'MYSQL_USER': 'csce483',
        'MYSQL_PASSWORD': 'Hogr!ders483',
    }
}

module.exports = nextConfig
