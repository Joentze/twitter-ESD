import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { UserDetailType, getUserDetail } from "../../helpers/user/userHelper";
import { ReadPostBodyType, getPostByUser } from "../../helpers/post/postHelper";
import { getLikesByPost } from "../../helpers/like/likeHelper";
import PostCard from "../../components/card/PostCard";
import {
  followUser,
  getFollowing,
  unfollowUser,
} from "../../helpers/follow/followHelper";
import { useAuth } from "../../auth/AuthContextProvider";
import SideBar from "../../nav/SideBar";
import { User, useAuth0 } from "@auth0/auth0-react";
const UserPage = () => {
  // const authId = useAuth();
  const { user } = useAuth0();
  const { userId } = useParams();
  const [userDetail, setUserDetail] = useState<UserDetailType>();
  const [posts, setPosts] = useState<ReadPostBodyType[]>([]);
  const [followers, setFollowers] = useState<string[]>([]);
  const [isFollowing, setIsFollowing] = useState<boolean>(false);
  useEffect(() => {
    const getContent = async () => {
      if (user) {
        try {
          const authId = (user as User)["sub"];
          const userResponse = await getUserDetail(userId as string);
          const myFollowers = await getFollowing(authId as string);
          const userFollowings = await getFollowing(userId as string);
          setFollowers(userFollowings);
          setUserDetail(userResponse);
          setIsFollowing(myFollowers.includes(userId as string));
          const postsResponse = await getPostByUser(userId as string);
          const postsTempArr: ReadPostBodyType[] = [];
          for (let post of postsResponse) {
            const thisPostLikes = await getLikesByPost(post["post id"]);
            postsTempArr.push({
              ...post,
              likes: thisPostLikes,
              "user detail": userResponse,
            });
          }
          postsTempArr.sort(
            (a, b) =>
              new Date(b["date posted"]).getTime() -
              new Date(a["date posted"]).getTime()
          );
          setPosts(postsTempArr);
        } catch (e) {
          setPosts([]);
        }
      }
    };
    getContent();
  }, [userId, user]);
  return (
    <div className="w-full h-screen flex flex-row">
      <div className="hidden xl:block lg:w-96 h-screen ">
        <SideBar />
      </div>
      <div className="grow border-l-2 border border-r-2 flex flex-col overflow-y-scroll">
        {userDetail ? (
          <div className="p-4 w-full h-fit flex flex-col gap-2 border-b-2 border">
            <div className="flex flex-row">
              <p className="font-bold text-3xl text-primary grow">
                @{(userDetail as UserDetailType).username}
              </p>
              <div className={user?.sub === userId ? "hidden" : "block"}>
                {isFollowing ? (
                  <button
                    className="btn btn-primary m-auto"
                    onClick={async () => {
                      await unfollowUser(user?.sub as string, userId as string);
                      setIsFollowing(false);
                    }}
                  >
                    Following
                  </button>
                ) : (
                  <button
                    className="btn btn-primary btn-outline m-auto"
                    onClick={async () => {
                      await followUser(user?.sub as string, userId as string);
                      setIsFollowing(true);
                    }}
                  >
                    Follow
                  </button>
                )}
              </div>
            </div>
            <p className="text-gray-600 ">
              Joined on{" "}
              {
                [
                  "Jan",
                  "Feb",
                  "Mar",
                  "Apr",
                  "May",
                  "Jun",
                  "Jul",
                  "Aug",
                  "Sep",
                  "Oct",
                  "Nov",
                  "Dec",
                ][
                  new Date(
                    (userDetail as UserDetailType)["user created on"]
                  ).getMonth()
                ]
              }{" "}
              {new Date(
                (userDetail as UserDetailType)["user created on"]
              ).getFullYear()}
            </p>
            <p className="text-sm text-gray-400">
              {(userDetail as UserDetailType)["user email"]}
            </p>
          </div>
        ) : (
          <></>
        )}
        {posts.map((post) => {
          return (
            <PostCard
              userDetail={post["user detail"]}
              postId={post["post id"]}
              postContent={post["post content"]}
              postImages={post["post images"]}
              postLocation={post["post location"]}
              posterId={post["poster id"]}
              datePosted={post["date posted"]}
              likes={post["likes"]}
            />
          );
        })}
      </div>
      <div className="hidden xl:block lg:w-96 h-screen "></div>
    </div>
  );
};
export default UserPage;
