import { useEffect, useState } from "react";
import SideBar from "../../nav/SideBar";
import { useAuth0 } from "@auth0/auth0-react";
import { UserDetailType, getAllUsers } from "../../helpers/user/userHelper";
import {
  followUser,
  getFollowing,
  unfollowUser,
} from "../../helpers/follow/followHelper";
import UserHeader from "../user/UserHeader";

const ExplorePage = () => {
  const { user } = useAuth0();
  const [following, setFollowing] = useState<string[]>([]);
  const [users, setUsers] = useState<UserDetailType[]>([]);
  useEffect(() => {
    const getFollowings = async () => {
      if (user) {
        const authId = user.sub;
        const followingsResponse = await getFollowing(authId as string);
        setFollowing(followingsResponse);
      }
    };
    getFollowings();
    const getUsers = async () => {
      const allUsers = await getAllUsers();
      console.log(allUsers);
      setUsers(allUsers);
    };
    getUsers();
  }, [user]);
  return (
    <div className="w-full h-screen flex flex-row">
      <div className="hidden xl:block lg:w-96 h-screen ">
        <SideBar />
      </div>
      <div className="grow border-l-2 border border-r-2 flex flex-col p-4 overflow-y-scroll">
        <p className="text-primary text-2xl font-bold">Find New Friends</p>
        <div className="divider"></div>
        {users.length && user ? (
          <>
            {users.map((userDetails) => {
              return (
                <>
                  {user.sub !== userDetails["user id"] ? (
                    <div className="border-b-2 p-4 flex flex-row">
                      <div className="grow">
                        <UserHeader
                          username={userDetails["username"]}
                          uid={userDetails["user id"]}
                        />
                      </div>
                      <>
                        {following.includes(userDetails["user id"]) ? (
                          <button
                            className="btn btn-primary btn-sm m-auto"
                            onClick={async () => {
                              await unfollowUser(
                                user?.sub as string,
                                userDetails["user id"] as string
                              );
                              const followingsResponse = await getFollowing(
                                user?.sub as string
                              );
                              setFollowing(followingsResponse);
                            }}
                          >
                            Following
                          </button>
                        ) : (
                          <button
                            className="btn btn-primary btn-sm btn-outline m-auto"
                            onClick={async () => {
                              await followUser(
                                user?.sub as string,
                                userDetails["user id"] as string
                              );
                              const followingsResponse = await getFollowing(
                                user?.sub as string
                              );
                              setFollowing(followingsResponse);
                            }}
                          >
                            Follow
                          </button>
                        )}
                      </>
                    </div>
                  ) : (
                    <></>
                  )}
                </>
              );
            })}
          </>
        ) : (
          <></>
        )}
      </div>
      <div className="hidden xl:block lg:w-96 h-screen "></div>
    </div>
  );
};
export default ExplorePage;
