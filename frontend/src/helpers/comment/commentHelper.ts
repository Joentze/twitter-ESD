import axios from "axios";
import { ResponseMessage } from "../helperTypes";

const API_ROUTE = "http://localhost:8000/api/v1";

export interface CommentBody {
  content: string;
  commenter_uid: string;
}

export interface CommentType {
  "comment id": string;
  "commenter uid": string;
  content: string;
  "date commented": string;
  "post id": string;
}

export const uploadComment = async (
  postId: string,
  commentBody: CommentBody
): Promise<CommentType> => {
  try {
    const response = await axios.post(
      `${API_ROUTE}/comment/upload/${postId}`,
      commentBody
    );
    return response.data["data"] as CommentType;
  } catch (e) {
    throw new Error("There was an error with uploading comment");
  }
};

export const getPostComments = async (
  postId: string
): Promise<CommentType[]> => {
  try {
    const response = await axios.get(`${API_ROUTE}/comment/${postId}`);
    return response.data["data"] as CommentType[];
  } catch (e) {
    throw new Error("There was an error with getting comments");
  }
};
