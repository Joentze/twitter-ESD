import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import FeedPage from "./pages/feed/FeedPage";
import PostPage from "./pages/post/PostPage";
import { AuthProvider } from "./auth/AuthContextProvider";
import UserPage from "./pages/user/UserPage";
import { Auth0Provider } from "@auth0/auth0-react";
import LoginButton from "./components/auth/LoginButton";
import CallbackPage from "./pages/callback/CallbackPage";
const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
const router = createBrowserRouter([
  {
    path: "/",
    element: (
      <>
        <LoginButton />
      </>
    ),
  },
  {
    path: "/callback",
    element: <CallbackPage />,
  },
  {
    path: "/feed",
    element: <FeedPage />,
  },
  {
    path: "/user/:userId",
    element: <UserPage />,
  },
  {
    path: "/post/:postId",
    element: <PostPage />,
  },
]);
root.render(
  <React.StrictMode>
    <Auth0Provider
      domain={"dev-eym6ylpoplxr2f0n.jp.auth0.com"}
      clientId={"LWkIEqZqSRPbq2yUrtLtSnS6gjjNidPw"}
      authorizationParams={{
        redirect_uri: "http://localhost:3000/callback",
      }}
    >
      <RouterProvider router={router} />
    </Auth0Provider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
