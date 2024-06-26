import { useState } from "react";
import { IoChatbubbleEllipses } from "react-icons/io5";
import { useAuth } from "../../auth/AuthContextProvider";
import {
  CommentBody,
  CommentType,
  uploadComment,
} from "../../helpers/comment/commentHelper";
import { useAuth0 } from "@auth0/auth0-react";
interface ICommentUploader {
  postId: string;
  comments: CommentType[];
  setComments: React.Dispatch<React.SetStateAction<CommentType[]>>;
}
const CommentUploader: React.FC<ICommentUploader> = ({
  postId,
  comments,
  setComments,
}) => {
  const [comment, setComment] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const { user } = useAuth0();
  const postComment = async () => {
    setLoading(true);
    const commentData = {
      commenter_uid: user?.sub as string,
      content: comment,
    };
    console.log(comments);
    await uploadComment(postId, commentData);
    setComment("");
    setLoading(false);
    window.location.reload();
  };
  return (
    <div className="w-full flex flex-row p-4 border border-b-2 gap-4">
      <label className="input input-bordered flex items-center gap-2 grow">
        <IoChatbubbleEllipses className="text-slate-600" />
        <input
          disabled={loading}
          defaultValue={comment}
          value={comment}
          onChange={(event) => setComment(event.target.value)}
          type="text"
          className="grow"
          placeholder="Example: 'Looks awesome!'"
        />
      </label>
      {loading ? (
        <span className="loading loading-spinner loading-md text-primary"></span>
      ) : (
        <button
          className="btn btn-primary"
          onClick={async () => await postComment()}
        >
          Comment
        </button>
      )}
    </div>
  );
};
export default CommentUploader;
