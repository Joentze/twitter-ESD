import React from "react";
import { UserDetailType } from "../../helpers/user/userHelper";
import { IoHeartOutline, IoChatboxOutline } from "react-icons/io5";
import { Link } from "react-router-dom";
import LikeButton from "../like/LikeButton";
import UserHeader from "../../pages/user/UserHeader";
interface IPostCard {
  postId: string;
  posterId: string;
  datePosted: string;
  postContent: string;
  postImages: string[];
  postLocation: string;
  likes?: string[];
  userDetail?: UserDetailType;
}
const PostCard: React.FC<IPostCard> = ({
  postContent,
  postId,
  postImages,
  postLocation,
  likes,
  datePosted,
  posterId,
  userDetail,
}) => {
  return (
    <div className="w-full h-fit flex flex-col p-2 border-b-2">
      <div className="w-full h-fit bg-gray flex flex-col p-2 gap-2">
        <div className="flex flex-col">
          <div className="flex flex-row">
            <UserHeader
              uid={posterId as string}
              username={(userDetail as UserDetailType).username}
            />
            <p className="text-right text-xs text-slate-300 m-auto">
              Posted on {new Date(datePosted).toDateString()}
            </p>
          </div>
          <p className="text-left text-xs italic text-slate-400">
            {postLocation}
          </p>
        </div>
        <p className="text-left justify text-slate-700 ">{postContent}</p>
        {postImages.length > 0 ? (
          <div className="w-full max-h-80 mt-2 carousel rounded-box">
            {postImages.map((image) => {
              return (
                <div className="carousel-item w-full">
                  <img
                    src={image}
                    className="bg-cover bg-center w-full h-full max-w-[800px]"
                    alt="Tailwind CSS Carousel component"
                  />
                </div>
              );
            })}
          </div>
        ) : (
          <></>
        )}
        <div className="flex flex-row gap-2 px-2">
          <div className="grow" />
          <Link to={`/post/${postId}`}>
            <button className="btn btn-square btn-ghost btn-sm">
              <IoChatboxOutline className="w-6 h-6 text-primary" />
            </button>
          </Link>
          <LikeButton postId={postId} userLikes={likes as string[]} />
        </div>
      </div>
    </div>
  );
};

export default PostCard;
