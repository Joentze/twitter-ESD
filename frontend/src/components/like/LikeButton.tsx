import React from "react";
import { useState } from "react";
import { useAuth } from "../../auth/AuthContextProvider";
import { IoHeartOutline, IoHeart } from "react-icons/io5";
import { likePost, unlikePost } from "../../helpers/like/likeHelper";
interface ILikeButton {
  postId: string;
  userLikes: string[];
}

const LikeButton: React.FC<ILikeButton> = ({ postId, userLikes }) => {
  const authId = useAuth();
  const [liked, setLiked] = useState<boolean>(userLikes.includes(authId));
  const onLikeClicked = async () => {
    if (liked) {
      unlikePost(postId, authId);
      setLiked(false);
    } else {
      likePost(postId, authId);
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
