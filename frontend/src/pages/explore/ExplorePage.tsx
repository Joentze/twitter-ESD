import SideBar from "../../nav/SideBar";

const ExplorePage = () => {
  return (
    <div className="w-full h-screen flex flex-row">
      <div className="hidden xl:block lg:w-96 h-screen ">
        <SideBar />
      </div>
      <div className="grow border-l-2 border border-r-2 flex flex-col p-4 overflow-y-scroll">
        <p className="text-primary text-2xl font-bold">Find New Friends</p>
        <div className="divider"></div>
      </div>
      <div className="hidden xl:block lg:w-96 h-screen "></div>
    </div>
  );
};
export default ExplorePage;
