import axios from "axios";
const API_ROUTE = "http://localhost:8000/api/v1";
interface FollowResponseDataType {
  "date followed": string;
  "followed id": string;
  "follower id": string;
}

interface FollowResponseType {
  code: number;
  data: FollowResponseDataType;
}

export const followUser = async (
  uid: string,
  followedId: string
): Promise<FollowResponseType> => {
  try {
    const response = await axios.post(`${API_ROUTE}/follow/${uid}`, {
      followed_id: followedId,
    });
    return response.data as FollowResponseType;
  } catch (e) {
    throw new Error("There was an error with following user");
  }
};

export const unfollowUser = async (
  uid: string,
  followedId: string
): Promise<FollowResponseType> => {
  try {
    const response = await axios.delete(`${API_ROUTE}/follow/${uid}`, {
      data: {
        followed_id: followedId,
      },
    });
    return response.data as FollowResponseType;
  } catch (e) {
    throw new Error("There was an error with following user");
  }
};

export const getFollowing = async (uid: string): Promise<string[]> => {
  try {
    const response = await axios.get(`${API_ROUTE}/follow/${uid}`);
    return response.data["data"] as string[];
  } catch (e) {
    throw new Error("There was an error with getting the following");
  }
};
