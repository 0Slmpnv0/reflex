import React from 'react'
import ReactDOM from 'react-dom/client'
import MainPage from './pages/MainPage.tsx'
import LoginPage from './pages/LoginPage.tsx'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './index.css'
import RegisterPage from './pages/RegisterPage.tsx'


const router = createBrowserRouter([
  {
    path: '/',
    element: <MainPage />
  },
  {
    path: 'log',
    element: <LoginPage />
  },
  {
    path: 'reg',
    element: <RegisterPage />
  }
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <RouterProvider  router={router} />
  </React.StrictMode>,
)
