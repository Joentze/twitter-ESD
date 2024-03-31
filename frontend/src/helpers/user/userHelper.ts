import axios from "axios";

const API_ROUTE = "http://localhost:8000/api/v1";

export interface UserDetailType {
  "is user private": number;
  "user created on": string;
  "user email": string;
  "user id": string;
  username: string;
}

export interface UserCreateReqBody {
  username: string;
  email: string;
}

export const getUserDetail = async (uid: string): Promise<UserDetailType> => {
  try {
    const response = await axios.get(`${API_ROUTE}/user/${uid}`);
    return response.data["data"] as UserDetailType;
  } catch (e) {
    throw new Error("There was an error with getting user data");
  }
};

export const createNewUser = async (
  uid: string,
  reqBody: UserCreateReqBody
): Promise<boolean> => {
  try {
    await axios.post(`${API_ROUTE}/user/${uid}`, reqBody);
    return true;
  } catch (e) {
    return false;
  }
};

export const getAllUsers = async (): Promise<UserDetailType[]> => {
  try {
    const response = await axios.get(`${API_ROUTE}/user/all`);
    return response.data["data"]["users"] as UserDetailType[];
  } catch (e) {
    throw new Error("There was an error getting all users");
  }
};
