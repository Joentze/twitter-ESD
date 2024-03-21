import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { UserDetailType, getUserDetail } from "../../helpers/user/userHelper";
import { ReadPostBodyType, getPostByUser } from "../../helpers/post/postHelper";
import { getLikesByPost } from "../../helpers/like/likeHelper";
import PostCard from "../../components/card/PostCard";
const UserPage = () => {
  const { userId } = useParams();
  const [userDetail, setUserDetail] = useState<UserDetailType>();
  const [posts, setPosts] = useState<ReadPostBodyType[]>([]);
  useEffect(() => {
    const getContent = async () => {
      const userResponse = await getUserDetail(userId as string);
      setUserDetail(userResponse);
      console.log(userResponse);
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
      setPosts(postsTempArr);
    };
    getContent();
  }, [userId]);
  return (
    <div className="w-full h-screen flex flex-row">
      <div className="hidden xl:block lg:w-96 h-screen "></div>
      <div className="grow border-l-2 border border-r-2 flex flex-col overflow-y-scroll">
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
