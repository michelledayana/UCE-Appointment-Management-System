import { AuthProvider } from '@/context/AuthContext';
import './globals.css';

export const metadata = {
  title: 'Sistema de Citas',
  description: 'Sistema de programación de citas médicas',
};

export default function RootLayout({ children }) {
  return (
    <html lang="es">
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}