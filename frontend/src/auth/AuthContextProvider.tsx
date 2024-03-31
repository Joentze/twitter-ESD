import React, { useContext, useState, createContext, useEffect } from "react";

//define the type of the context
// interface AuthContextProps {
//   authId: string;
//   setAuthId: (id: string) => void;
// }

// create the context
const AuthContext = createContext<string | undefined>(undefined);

export const AuthProvider: React.FC<any> = ({ children }) => {
  const [authId, setAuthId] = useState<string>(
    "google-oauth2|106331917938998415796"
  );

  // value to pass to authProvider
  //   const value = { authId, setAuthId };
  //   const getStringFromLocalStorage = () => {
  //     const storedData = localStorage.getItem("twitter_auth");
  //     if (storedData) {
  //       const stringedData = JSON.stringify(storedData).replace(/&#39;/g, `"`);
  //       console.log(stringedData);
  //       const parsedData = JSON.parse(stringedData);
  //       console.log(parsedData);
  //       setAuthId(parsedData.sub);
  //     }
  //   };

  //   useEffect(() => {
  //     getStringFromLocalStorage();
  //   }, []);

  return <AuthContext.Provider value={authId}>{children}</AuthContext.Provider>;
};

// Hook to make it easy to use the context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useauth must be used within a authProvider");
  }
  return context;
};
