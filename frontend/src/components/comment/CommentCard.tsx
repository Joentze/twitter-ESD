import React, { useEffect, useState } from "react";
import { UserDetailType, getUserDetail } from "../../helpers/user/userHelper";
import UserHeader from "../../pages/user/UserHeader";

interface ICommentCard {
  commentId: string;
  commenterUid: string;
  content: string;
  dateCommented: string;
  postId: string;
}
const CommentCard: React.FC<ICommentCard> = ({
  commentId,
  commenterUid,
  content,
  dateCommented,
  postId,
}) => {
  const [userData, setUserData] = useState<UserDetailType>();
  useEffect(() => {
    const getUser = async () => {
      const userDataResponse = await getUserDetail(commenterUid);
      setUserData(userDataResponse);
    };
    getUser();
  }, []);
  return (
    <div className="w-full max-h-24 h-fit p-4 flex flex-col gap-2 border border-b-2">
      <div className="flex flex-row">
        <UserHeader
          username={userData?.username as string}
          uid={commenterUid}
        />
        <p className="text-right text-xs text-slate-300 m-auto">
          Commented on {new Date(dateCommented).toDateString()}
        </p>
      </div>
      <p className="text-slate-700">{content}</p>
    </div>
  );
};
export default CommentCard;
