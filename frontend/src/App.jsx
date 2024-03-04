import MainPage from "./pages/MainPage/MainPage";
import {Route, Routes} from "react-router";
import SignInPage from "./pages/SignInPage/SignInPage";
import React from "react";
import MainLayout from "./pages/MainLayout/MainLayout";
import SignUpPage from "./pages/SignUpPage/SignUpPage";

const App = () => {

    return (
            <Routes>
                 {/*mainRoute*/}
                <Route path="/" element={<MainLayout/>}>
                    <Route index path="/main" element={<MainPage/>}/>
                </Route>
                {/*Auth*/}
                <Route path="/panel/">
                    <Route path="signin" element={<SignInPage/>}/>
                    <Route path="signup" element={<SignUpPage/>}/>
                    <Route path="recovery"/>
                </Route>
            </Routes>
        )
};

export default App;
