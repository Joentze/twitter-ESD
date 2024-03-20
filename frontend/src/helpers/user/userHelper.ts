import axios from "axios";

const API_ROUTE = "http://localhost:8000/api/v1";

export interface UserDetailType {
  "is user private": number;
  "user created on": string;
  "user email": string;
  "user id": string;
  username: string;
}

export const getUserDetail = async (uid: string): Promise<UserDetailType> => {
  try {
    const response = await axios.get(`${API_ROUTE}/user/${uid}`);
    return response.data["data"] as UserDetailType;
  } catch (e) {
    throw new Error("There was an error with getting user data");
  }
};
