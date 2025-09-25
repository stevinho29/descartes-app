import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';


import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import WelcomePage from './welcome_page';
import PortfolioForm from './portfolio_form';
import PortfolioSummary from './portfolio_summary';

const router = createBrowserRouter([
  {
    path: "/",
    element: <WelcomePage />,
  }, {
    path: "/form",
    element: <PortfolioForm />
  }, {
    path: "/form/:contactId",
    element: <PortfolioForm />
  }, {
    path: "/summary",
    element: <PortfolioSummary />
  }
])

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
