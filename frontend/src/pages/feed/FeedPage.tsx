import React from "react";
import logo from "./logo.svg";

import PostDisplay from "../../components/displays/PostDisplay";
import PostUploader from "../../components/uploader/PostUploader";
import SideBar from "../../nav/SideBar";
const FeedPage = () => {
  return (
    <div className="App">
      <div className="w-full h-screen flex flex-row">
        <div className="hidden xl:block lg:w-96 h-screen ">
          <SideBar />
        </div>
        <div className="grow border-l-2 border border-r-2 flex flex-col">
          <PostUploader />

          <PostDisplay />
        </div>
        <div className="hidden xl:block lg:w-96 h-screen "></div>
      </div>
    </div>
  );
};

export default FeedPage;
