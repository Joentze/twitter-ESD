import { useEffect, useState } from "react";
import React from "react";
import { ReadPostBodyType, readAllPosts } from "../../helpers/post/postHelper";
import PostCard from "../card/PostCard";
import { User, useAuth0 } from "@auth0/auth0-react";
import PostUploader from "../../components/uploader/PostUploader";
const PostDisplay = () => {
  const { user } = useAuth0();

  const [loading, setLoading] = useState<boolean>(false);
  const [posts, setPosts] = useState<ReadPostBodyType[]>([]);
  useEffect(() => {
    const getPosts = async () => {
      if (user) {
        try {
          const authId = (user as User)["sub"];
          const responsePosts = await readAllPosts(authId as string);
          const { data } = responsePosts;
          data.sort(
            (a, b) =>
              new Date(b["date posted"]).getTime() -
              new Date(a["date posted"]).getTime()
          );
          setPosts(data);
          setLoading(false);
        } catch (e) {
          setPosts([]);
        }
      }
    };
    getPosts();
  }, [user]);
  return (
    <>
      <PostUploader />
      <div className="overflow-y-scroll">
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
    </>
  );
};

export default PostDisplay;
