import React, { useEffect } from "react";
import { useState } from "react";
import { useAuth } from "../../auth/AuthContextProvider";
import { IoHeartOutline, IoHeart } from "react-icons/io5";
import { likePost, unlikePost } from "../../helpers/like/likeHelper";
import { User, useAuth0 } from "@auth0/auth0-react";
interface ILikeButton {
  postId: string;
  userLikes: string[];
}

const LikeButton: React.FC<ILikeButton> = ({ postId, userLikes }) => {
  const { user } = useAuth0();
  const [liked, setLiked] = useState<boolean>(false);
  useEffect(() => {
    if (user) {
      setLiked(userLikes.includes(user.sub as string));
    }
  }, [user]);
  const onLikeClicked = async () => {
    if (user)
      if (liked) {
        unlikePost(postId, user.sub as string);
        setLiked(false);
      } else {
        likePost(postId, user.sub as string);
        setLiked(true);
      }
  };
  return (
    <button
      className="btn btn-square btn-ghost btn-sm"
      onClick={async () => await onLikeClicked()}
    >
      {liked ? (
        <IoHeart className="w-6 h-6 text-primary" />
      ) : (
        <IoHeartOutline className="w-6 h-6 text-primary" />
      )}
    </button>
  );
};

export default LikeButton;
