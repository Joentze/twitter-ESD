import { useState } from "react";
import { IoChatbubbleEllipses } from "react-icons/io5";
import { useAuth } from "../../auth/AuthContextProvider";
import { uploadComment } from "../../helpers/comment/commentHelper";
interface ICommentUploader {
  postId: string;
}
const CommentUploader: React.FC<ICommentUploader> = ({ postId }) => {
  const [comment, setComment] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);
  const authId = useAuth();
  const postComment = async () => {
    setLoading(true);
    await uploadComment(postId, {
      commenter_uid: authId,
      content: comment,
    });
    setComment("");
    setLoading(false);
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
