import { createContext, useContext } from "react";

// Step 1: Create a new React context
export const MyContext = createContext<string | undefined>(undefined);

export const AuthContext = () => useContext(MyContext);

// export { MyContextProvider, useMyContext };
