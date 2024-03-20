import { useParams } from "react-router-dom";
import PostDisplay from "../../components/displays/PostDisplay";
import { useEffect, useState } from "react";
import {
  CommentType,
  getPostComments,
} from "../../helpers/comment/commentHelper";
import { ReadPostBodyType, getPost } from "../../helpers/post/postHelper";
import PostCard from "../../components/card/PostCard";
import { UserDetailType, getUserDetail } from "../../helpers/user/userHelper";

const PostPage = () => {
  const { postId } = useParams();
  const [post, setPost] = useState<ReadPostBodyType>();
  const [userDetail, setUserDetail] = useState<UserDetailType>();
  const [comments, setComments] = useState<CommentType[]>([]);
  useEffect(() => {
    const getPostContent = async () => {
      const commentsData = await getPostComments(postId as string);
      const postData = await getPost(postId as string);
      const uid = postData["poster id"];
      const userData = await getUserDetail(uid);
      setUserDetail(userData);
      setPost(postData);
      setComments(commentsData);
    };
    getPostContent();
  }, [postId]);
  return (
    <div className="w-full h-screen flex flex-row">
      <div className="hidden xl:block lg:w-96 h-screen "></div>
      <div className="grow border-l-2 border border-r-2 flex flex-col">
        {post && userDetail ? (
          <PostCard
            userDetail={userDetail}
            postId={post["post id"]}
            postContent={post["post content"]}
            postImages={post["post images"]}
            postLocation={post["post location"]}
            posterId={post["poster id"]}
            datePosted={post["date posted"]}
          />
        ) : (
          <></>
        )}
      </div>
      <div className="hidden xl:block lg:w-96 h-screen "></div>
    </div>
  );
};

export default PostPage;
