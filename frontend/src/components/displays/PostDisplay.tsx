import { useEffect, useState } from "react";
import React from "react";
import { ReadPostBodyType, readAllPosts } from "../../helpers/post/postHelper";
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
  return <></>;
};

export default PostDisplay;
