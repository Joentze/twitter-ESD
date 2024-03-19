import React from "react";
import logo from "./logo.svg";
import "./App.css";
import PostDisplay from "./components/displays/PostDisplay";

function App() {
  return (
    <div className="App">
      <div className="w-full h-screen flex flex-row">
        <div className="hidden xl:block lg:w-96 h-screen "></div>
        <div className="grow border-l-2 border border-r-2 flex flex-col gap-4 pt-10">
          <PostDisplay />
        </div>
        <div className="hidden xl:block lg:w-96 h-screen "></div>
      </div>
    </div>
  );
}

export default App;
