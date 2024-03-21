import axios from "axios";
import { ResponseMessage } from "../helperTypes";
import { UserDetailType } from "../user/userHelper";

const API_ROUTE = "http://localhost:8000/api/v1";

interface PostBodyType {
  post_content: string;
  post_location: string;
  post_images: string[];
}

export interface ReadPostBodyType {
  likes?: string[];
  "user detail"?: UserDetailType;
  "date posted": string;
  "post content": string;
  "post id": string;
  "post images": string[];
  "post location": string;
  "poster id": string;
}

interface ReadAllPostResponseType {
  code: number;
  data: ReadPostBodyType[];
}

export const uploadPost = async (
  uid: string,
  postBody: PostBodyType
): Promise<ResponseMessage> => {
  try {
    const response = await axios.post(
      `${API_ROUTE}/post/upload/${uid}`,
      postBody
    );
    return response.data as ResponseMessage;
  } catch (e) {
    throw new Error("There was an error with uploading post");
  }
};

export const readAllPosts = async (
  uid: string
): Promise<ReadAllPostResponseType> => {
  try {
    const response = await axios.get(`${API_ROUTE}/read_posts`, {
      headers: { uid },
    });
    return response.data as ReadAllPostResponseType;
  } catch (e) {
    throw new Error("There was an error with reading your posts");
  }
};

export const getPost = async (postId: string): Promise<ReadPostBodyType> => {
  try {
    const response = await axios.get(`${API_ROUTE}/post/${postId}`);
    return response.data["data"] as ReadPostBodyType;
  } catch (e) {
    throw new Error("There was an error with getting the post at this moment");
  }
};

export const getPostByUser = async (
  uid: string
): Promise<ReadPostBodyType[]> => {
  try {
    const response = await axios.get(`${API_ROUTE}/post/user_get/${uid}`);
    return response.data["data"] as ReadPostBodyType[];
  } catch (e) {
    throw new Error("There was an error with getting posts from user");
  }
};
