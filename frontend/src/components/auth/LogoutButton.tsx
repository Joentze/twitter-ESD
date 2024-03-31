import React from "react";
import { useAuth0 } from "@auth0/auth0-react";
import { IoLogOutOutline } from "react-icons/io5";

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <div
      className="w-full hover:bg-gray-200 h-fit rounded-lg p-4 flex flex-row gap-2 text-primary text-lg"
      onClick={() =>
        logout({ logoutParams: { returnTo: "http://localhost:3000/" } })
      }
    >
      <IoLogOutOutline className="w-6 h-6" />
      Logout
    </div>
  );
};

export default LogoutButton;
