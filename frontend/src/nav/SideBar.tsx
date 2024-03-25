import YapperIcon from "../misc/YapperIcon";
import { useLocation } from "react-router-dom";
import { IoNewspaper, IoCompass, IoPersonSharp } from "react-icons/io5";
import { Link } from "react-router-dom";
import { useAuth } from "../auth/AuthContextProvider";
const SideBar = () => {
  const location = useLocation();
  const authId = useAuth();
  return (
    <>
      <div className="flex flex-col ml-24 p-6">
        <div className="ml-4 flex flex-row w-20">
          <YapperIcon />
          <p className="text-md font-bold text-primary m-auto">.com</p>
        </div>
        <div className="divider"></div>
        <Link to="/feed">
          <div
            className={`${
              location.pathname.includes("/feed") ? "font-bold" : ""
            } w-full hover:bg-gray-200 h-fit rounded-lg p-4 flex flex-row gap-2 text-primary text-lg`}
          >
            <IoNewspaper className="w-6 h-6" />
            Your Feed
          </div>
        </Link>
        <Link to="/explore">
          <div
            className={`${
              location.pathname.includes("/explore") ? "font-bold" : ""
            } w-full hover:bg-gray-200 h-fit rounded-lg p-4 flex flex-row gap-2 text-primary text-lg`}
          >
            <IoCompass className="w-6 h-6" />
            Explore
          </div>
        </Link>

        <Link to={`/user/${authId}`}>
          <div
            className={`${
              location.pathname.includes(`/user/${encodeURIComponent(authId)}`)
                ? "font-bold"
                : ""
            } w-full hover:bg-gray-200 h-fit rounded-lg p-4 flex flex-row gap-2 text-primary text-lg`}
          >
            <IoPersonSharp className="w-6 h-6" />
            Your Profile
          </div>
        </Link>
      </div>
    </>
  );
};

export default SideBar;
