import { useEffect, useState } from "react";
import React from "react";
import { ReadPostBodyType, readAllPosts } from "../../helpers/post/postHelper";
import PostCard from "../card/PostCard";
import { useAuth } from "../../auth/AuthContextProvider";
const PostDisplay = () => {
  const authId = useAuth();
  const [loading, setLoading] = useState<boolean>(false);
  const [posts, setPosts] = useState<ReadPostBodyType[]>([]);
  useEffect(() => {
    const getPosts = async () => {
      const responsePosts = await readAllPosts(authId as string);
      const { data } = responsePosts;
      console.log(data);
      setPosts(data);
      setLoading(false);
    };
    getPosts();
  }, []);
  return (
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
  );
};

export default PostDisplay;
