import axios from "axios";

const API_ROUTE = "http://localhost:8000/api/v1";
const BUCKET_ROUTE = "http://localhost:9000";

export const uploadFile = async (file: File): Promise<string> => {
  try {
    checkIfImage(file);
    let formData = new FormData();
    formData.append("file", file);
    const response = await axios.post(`${API_ROUTE}/asset/upload`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    const objectName = response.data["data"]["object_name"];
    return `${BUCKET_ROUTE}/images/${objectName}`;
  } catch (e) {
    throw new Error((e as Error).message as string);
  }
};

export const checkIfImage = (file: File): void => {
  const filename = file.name;
  const imageExtensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp"];
  const extension = filename
    .slice(((filename.lastIndexOf(".") - 1) >>> 0) + 2)
    .toLowerCase();
  if (!imageExtensions.includes(`.${extension}`))
    throw new Error("File uploaded is not an image");
};
