import React from "react";
import logo from "./logo.svg";

import PostDisplay from "../../components/displays/PostDisplay";

const FeedPage = () => {
  return (
    <div className="App">
      <div className="w-full h-screen flex flex-row" data-theme="light">
        <div className="hidden xl:block lg:w-96 h-screen "></div>
        <div className="grow border-l-2 border border-r-2 flex flex-col">
          <div className="w-full h-24 border border-b-2"></div>
          <PostDisplay />
        </div>
        <div className="hidden xl:block lg:w-96 h-screen "></div>
      </div>
    </div>
  );
};

export default FeedPage;
