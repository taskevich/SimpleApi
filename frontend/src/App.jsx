import MainPage from "./pages/MainPage/MainPage";
import {Route, Routes} from "react-router";
import SignInPage from "./pages/SignInPage/SignInPage";
import React from "react";
import MainLayout from "./pages/MainLayout/MainLayout";
import SignUpPage from "./pages/SignUpPage/SignUpPage";
import TariffsPage from "./pages/TariffsPage/TariffsPage";
import AboutPage from "./pages/AboutPage/AboutPage";

const App = () => {

    return (
            <Routes>
                 {/*mainRoute*/}
                <Route path="/" element={<MainLayout/>}>
                    <Route index element={<MainPage/>}/>
                    <Route path="tariffs" element={<TariffsPage/>}/>
                    <Route path="about" element={<AboutPage/>}/>
                </Route>
                {/*Panel*/}
                <Route path="/panel/">
                    <Route path="signin" element={<SignInPage/>}/>
                    <Route path="signup" element={<SignUpPage/>}/>
                    <Route path="recovery"/>
                </Route>
            </Routes>
        )
};

export default App;
