import React from "react";
import { Link } from "react-router-dom";
interface IUserHeader {
  uid: string;
  username: string;
}

const UserHeader: React.FC<IUserHeader> = ({ uid, username }) => {
  return (
    <Link to={`/user/${uid}`}>
      <p className="text-left text-md font-bold text-slate-600 text-lg grow hover:underline">
        @{username}
      </p>
    </Link>
  );
};
export default UserHeader;
