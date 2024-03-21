import { useParams } from "react-router-dom";
import PostDisplay from "../../components/displays/PostDisplay";
import { useEffect, useState } from "react";
import { IoChatbubbleEllipses } from "react-icons/io5";

import {
  CommentType,
  getPostComments,
} from "../../helpers/comment/commentHelper";
import { ReadPostBodyType, getPost } from "../../helpers/post/postHelper";
import PostCard from "../../components/card/PostCard";
import { UserDetailType, getUserDetail } from "../../helpers/user/userHelper";
import CommentCard from "../../components/comment/CommentCard";
import { getLikesByPost } from "../../helpers/like/likeHelper";

const PostPage = () => {
  const { postId } = useParams();
  const [post, setPost] = useState<ReadPostBodyType>();
  const [userDetail, setUserDetail] = useState<UserDetailType>();
  const [comments, setComments] = useState<CommentType[]>([]);
  const [likes, setLikes] = useState<string[]>([]);
  useEffect(() => {
    const getPostContent = async () => {
      const commentsData = await getPostComments(postId as string);
      const postData = await getPost(postId as string);
      const uid = postData["poster id"];
      const userData = await getUserDetail(uid);
      const likesResponse = await getLikesByPost(postId as string);
      setLikes(likesResponse);
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
            likes={likes}
          />
        ) : (
          <></>
        )}
        <div className="w-full flex flex-row p-4 border border-b-2 gap-4">
          <label className="input input-bordered flex items-center gap-2 grow">
            <IoChatbubbleEllipses className="text-slate-600" />
            <input
              type="text"
              className="grow"
              placeholder="Example: 'Looks awesome!'"
            />
          </label>
          <button className="btn btn-primary">Comment</button>
        </div>
        <>
          {comments.map((comment) => {
            return (
              <CommentCard
                commentId={comment["comment id"]}
                commenterUid={comment["commenter uid"]}
                content={comment["content"]}
                dateCommented={comment["date commented"]}
                postId={comment["post id"]}
              />
            );
          })}
        </>
      </div>

      <div className="hidden xl:block lg:w-96 h-screen "></div>
    </div>
  );
};

export default PostPage;
