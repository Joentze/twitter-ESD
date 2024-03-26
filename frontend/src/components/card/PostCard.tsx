import React from "react";
interface IPostCard {
  postId: string;
  posterId: string;
  datePosted: string;
  postContent: string;
  postImages: string[];
  postLocation: string;
  likes: string[];
}
const PostCard: React.FC<IPostCard> = ({
  postContent,
  postId,
  postImages,
  postLocation,
  likes,
  datePosted,
  posterId,
}) => {
  return (
    <div className="w-full h-fit flex flex-col">
      <div className="w-full h-16 bg-gray flex flex-row">{postContent}</div>
    </div>
  );
};

export default PostCard;
