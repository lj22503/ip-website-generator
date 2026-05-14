import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Personal IP Generator - Create Your Personal Website',
  description: 'Generate a beautiful personal IP website based on your MBTI type and story. Powered by AI.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  );
}
