import { useEffect, useState } from "react";
import React from "react";
import { ReadPostBodyType, readAllPosts } from "../../helpers/post/postHelper";
import PostCard from "../card/PostCard";
const PostDisplay = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [posts, setPosts] = useState<ReadPostBodyType[]>([]);
  useEffect(() => {
    const getPosts = async () => {
      const responsePosts = await readAllPosts("user1_uid");
      const { data } = responsePosts;
      console.log(data);
      setPosts(data);
      setLoading(false);
    };
    getPosts();
  }, []);
  return (
    <>
      {posts.map((post) => {
        return (
          <PostCard
            postId={post["post id"]}
            postContent={post["post content"]}
            postImages={post["likes"]}
            postLocation={post["post location"]}
            posterId={post["poster id"]}
            datePosted={post["date posted"]}
            likes={post["likes"]}
          />
        );
      })}
    </>
  );
};

export default PostDisplay;