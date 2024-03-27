import axios from "axios";
import { ResponseMessage } from "../helperTypes";

const API_ROUTE = "http://localhost:8000/api/v1";

interface LikeResponseType {
  code: number;
  data: LikeDataResponseType;
}

interface LikeDataResponseType {
  "date liked": string;
  "post id": string;
  "user id": string;
}

export const likePost = async (
  postId: string,
  uid: string
): Promise<LikeResponseType> => {
  try {
    const response = await axios.post(`${API_ROUTE}/like/${postId}`, { uid });
    return response.data as LikeResponseType;
  } catch (e) {
    throw new Error("There was an error with liking post");
  }
};

export const unlikePost = async (
  postId: string,
  uid: string
): Promise<LikeResponseType> => {
  try {
    const response = await axios.delete(`${API_ROUTE}/like/${postId}`, {
      data: { uid },
    });
    return response.data as LikeResponseType;
  } catch (e) {
    throw new Error("There was an error with liking post");
  }
};

export const getLikesByPost = async (postId: string): Promise<string[]> => {
  try {
    const response = await axios.get(`${API_ROUTE}/like/${postId}`);
    if (response.data["data"] !== undefined) {
      return response.data["data"] as string[];
    } else {
      return [];
    }
  } catch (e) {
    throw new Error("There was an error with getting likes for the post");
  }
};
