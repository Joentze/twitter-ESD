import { User, useAuth0 } from "@auth0/auth0-react";
import { useEffect } from "react";
import { createNewUser } from "../../helpers/user/userHelper";
import { useNavigate } from "react-router-dom";

const CallbackPage = () => {
  const { user, isAuthenticated } = useAuth0();
  const navigate = useNavigate();
  useEffect(() => {
    const onCallback = async () => {
      if (isAuthenticated) {
        const { sub, email, nickname } = user as User;
        const response = await createNewUser(sub as string, {
          email: email as string,
          username: nickname as string,
        });
        navigate("/feed");
        if (!response) console.log("User already exists");
        navigate("/feed");
      }
    };
    onCallback();
  }, [user]);
  return (
    <div className="w-full h-screen flex">
      <span className="loading loading-spinner loading-lg m-auto loading-primary"></span>
    </div>
  );
};
export default CallbackPage;
