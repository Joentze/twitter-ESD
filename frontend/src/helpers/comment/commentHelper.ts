import axios from "axios";
import { ResponseMessage } from "../helperTypes";

const API_ROUTE = "http://localhost:8000/api/v1";

interface CommentBody {
  content: string;
  commenter_uid: string;
}

export const uploadComment = async (
  postId: string,
  commentBody: CommentBody
): Promise<ResponseMessage> => {
  try {
    const response = await axios.post(
      `${API_ROUTE}/comment/upload/${postId}`,
      commentBody
    );
    return response.data as ResponseMessage;
  } catch (e) {
    throw new Error("There was an error with uploading comment");
  }
};
