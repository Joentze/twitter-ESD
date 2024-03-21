import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import reportWebVitals from "./reportWebVitals";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import FeedPage from "./pages/feed/FeedPage";
import PostPage from "./pages/post/PostPage";
import { AuthProvider } from "./auth/AuthContextProvider";
import UserPage from "./pages/user/UserPage";
const root = ReactDOM.createRoot(
  document.getElementById("root") as HTMLElement
);
const router = createBrowserRouter([
  {
    path: "/",
    element: <>hello world</>,
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
    <AuthProvider>
      <RouterProvider router={router} />
    </AuthProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
