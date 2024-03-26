import { useNavigate, useParams } from "react-router-dom";
import PostDisplay from "../../components/displays/PostDisplay";
import { useEffect, useState } from "react";
import { IoArrowBack } from "react-icons/io5";

import {
  CommentType,
  getPostComments,
} from "../../helpers/comment/commentHelper";
import { ReadPostBodyType, getPost } from "../../helpers/post/postHelper";
import PostCard from "../../components/card/PostCard";
import { UserDetailType, getUserDetail } from "../../helpers/user/userHelper";
import CommentCard from "../../components/comment/CommentCard";
import { getLikesByPost } from "../../helpers/like/likeHelper";
import CommentUploader from "../../components/uploader/CommentUploader";

const PostPage = () => {
  const navigate = useNavigate();
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
      <div className="hidden xl:block lg:w-96 h-screen flex flex-col">
        <div className="flex flex-row p-4">
          <div className="grow"></div>
          <button
            className="btn btn-square btn-ghost"
            onClick={() => navigate(-1)}
          >
            <IoArrowBack className="w-6 h-6 text-gray-400" />
          </button>
        </div>
      </div>
      <div className="grow border-l-2 border border-r-2 flex flex-col">
        {post && userDetail ? (
          <>
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
            <CommentUploader
              postId={post["post id"]}
              comments={comments}
              setComments={setComments}
            />
          </>
        ) : (
          <></>
        )}

        <div className="overflow-y-scroll">
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
        </div>
      </div>

      <div className="hidden xl:block lg:w-96 h-screen "></div>
    </div>
  );
};

export default PostPage;
