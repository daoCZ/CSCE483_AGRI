/*
import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
 // title: ,
 // description: ,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>{children}</body>
    </html>
  )
}
*/
import styles from "./utils.module.css";
import Link from "next/link"

export default function RootLayout({ children }:{ children: React.ReactNode }) {
  return (
    <html>
      <head />
      <body>
        <div className={`${styles.sidebar}`}>
          <Link href="/">Home</Link>
          <Link href="/node_list">Node List</Link>
          <Link href="/report">Report Generator</Link>
        </div>
        <div className={`${styles.content}`}>
          {children}
        </div>
      </body>
    </html>
  )
}