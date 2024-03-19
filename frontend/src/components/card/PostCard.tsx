import React from "react";
import { UserDetailType } from "../../helpers/user/userHelper";
interface IPostCard {
  postId: string;
  posterId: string;
  datePosted: string;
  postContent: string;
  postImages: string[];
  postLocation: string;
  likes: string[];
  userDetail: UserDetailType;
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
      <div className="w-full h-16 bg-gray flex flex-row"></div>
    </div>
  );
};

export default PostCard;
