import { ChangeEvent, useState } from "react";
import {
  IoImageSharp,
  IoNavigateCircle,
  IoCloseOutline,
} from "react-icons/io5";
import { uploadFile } from "../../helpers/asset/assetHelper";
const PostUploader = () => {
  const [locationOpen, setLocationOpen] = useState<boolean>(false);
  const [fileList, setFileList] = useState<string[]>([]);
  const [showCancel, setShowCancel] = useState<boolean>(false);
  const [postContent, setPostContent] = useState<string>("");
  const [postLocation, setPostLocation] = useState<string>("");
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
  const makePost = async () => {};
  return (
    <div className="w-full h-fit p-4 flex flex-col border border-b-2 ">
      <textarea
        className="textarea textarea-bordered"
        placeholder="Make a Post!"
        defaultValue={postContent}
        onChange={(event) => setPostContent(event.target.value)}
      ></textarea>
      <input
        className={`${
          locationOpen ? "block" : "hidden"
        } w-full input input-sm input-bordered mt-4`}
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
        <button className="btn btn-primary btn-sm">Post</button>
      </div>
    </div>
  );
};
export default PostUploader;
