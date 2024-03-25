import { ChangeEvent, useState } from "react";
import {
  IoImageSharp,
  IoNavigateCircle,
  IoCloseOutline,
} from "react-icons/io5";
import { uploadFile } from "../../helpers/asset/assetHelper";
import { uploadPost } from "../../helpers/post/postHelper";
import { useAuth } from "../../auth/AuthContextProvider";
import { useAuth0 } from "@auth0/auth0-react";
const PostUploader = () => {
  // const authId = useAuth();
  const { user } = useAuth0();
  const [locationOpen, setLocationOpen] = useState<boolean>(false);
  const [uploading, setUploading] = useState<boolean>(false);
  const [fileList, setFileList] = useState<string[]>([]);
  const [showCancel, setShowCancel] = useState<boolean>(false);
  const [postContent, setPostContent] = useState<string>("");
  const [postLocation, setPostLocation] = useState<string>("Singapore");
  const onFileUpload = async (event: ChangeEvent) => {
    const target = event.target as HTMLInputElement;
    if (target.files) {
      try {
        let urls: string[] = [];
        const files = target.files;
        Array.from(files).forEach(async (file: File) =>
          urls.push(await uploadFile(file))
        );
        setFileList(urls);
        setShowCancel(true);
      } catch (e) {
        throw new Error((e as Error).message as string);
      }
    }
  };
  const clearImages = () => {
    (document.getElementById("post-file-uploader") as HTMLInputElement).value =
      "";
    setFileList([]);
    setShowCancel(false);
  };
  const makePost = async () => {
    try {
      if (postContent !== "") setUploading(true);
      console.log({
        post_content: postContent,
        post_location: postLocation,
        post_images: fileList,
      });
      await uploadPost(user?.sub as string, {
        post_content: postContent,
        post_location: postLocation,
        post_images: fileList,
      });

      setPostContent("");
      setPostLocation("Singapore");
      (
        document.getElementById("post-file-uploader") as HTMLInputElement
      ).value = "";
      setFileList([]);
      setUploading(false);
    } catch (e) {
      throw new Error((e as Error).message);
    }
  };
  return (
    <div className="w-full h-fit p-4 flex flex-col border border-b-2 ">
      <textarea
        className="textarea textarea-bordered textarea-primary border-2"
        placeholder="Make a Post!"
        value={postContent}
        defaultValue={postContent}
        onChange={(event) => setPostContent(event.target.value)}
      ></textarea>
      <input
        className={`${
          locationOpen ? "block" : "hidden"
        } w-full input input-sm input-bordered mt-4 input-primary`}
        value={postLocation}
        defaultValue={postLocation}
        onChange={(event) => setPostLocation(event.target.value)}
        placeholder="Your Location"
      ></input>
      <div className="divider"></div>
      <div className="flex flex-row gap-2">
        <button
          className="btn btn-square btn-sm btn-ghost "
          onClick={() => setLocationOpen(!locationOpen)}
        >
          <IoNavigateCircle className="w-6 h-6 text-primary" />
        </button>
        <div className="divider divider-horizontal -mx-2"></div>
        <input
          id="post-file-uploader"
          multiple
          type="file"
          onChange={async (event) => await onFileUpload(event)}
          className="file-input-primary file-input file-input-bordered btn-gray-600  w-full max-w-xs file-input-xs m-auto"
        />
        <button
          className={`${
            showCancel ? "block" : "hidden"
          } btn btn-square btn-sm btn-ghost `}
          onClick={clearImages}
        >
          <IoCloseOutline className="ml-1 w-6 h-6 text-primary" />
        </button>
        <div className="grow"></div>
        {uploading ? (
          <span className="loading loading-spinner loading-md text-primary"></span>
        ) : (
          <button
            disabled={postContent.length === 0}
            className="btn btn-primary btn-sm"
            onClick={async () => await makePost()}
          >
            Post
          </button>
        )}
      </div>
    </div>
  );
};
export default PostUploader;
