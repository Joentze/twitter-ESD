import axios from "axios";
import { url } from "inspector";

const API_ROUTE = "http://localhost:8000/api/v1";

interface PostBodyType {
  post_content: string;
  post_location: string;
  post_images: string[];
}

interface ResponseMessage {
  code: number;
  message: string;
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

