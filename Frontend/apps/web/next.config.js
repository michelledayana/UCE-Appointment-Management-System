const path = require('path')

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  images: {
    domains: ['localhost'],
  },
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  },
  webpack: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@/contexts': path.resolve(__dirname, '../../shared/contexts'),
      '@/components': path.resolve(__dirname, '../../shared/components'),
      '@/lib': path.resolve(__dirname, '../../shared/lib'),
      '@/types': path.resolve(__dirname, '../../shared/types'),
    }
    return config
  },
}

module.exports = nextConfig
