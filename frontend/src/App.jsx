import MainPage from "./pages/MainPage/MainPage";
import {Route, Routes} from "react-router";
import SignInPage from "./pages/SignInPage/SignInPage";
import React from "react";
import MainLayout from "./pages/Layout/MainLayout/MainLayout";
import SignUpPage from "./pages/SignUpPage/SignUpPage";
import TariffsPage from "./pages/TariffsPage/TariffsPage";
import AboutPage from "./pages/AboutPage/AboutPage";
import {UserProvider} from "./utils/lib/Auth/UserContext";
import AuthLayout from "./pages/Layout/AuthLayout/AuthLayout";





const App = () => {

    return (
        <UserProvider>
            <Routes>
                 {/*mainRoute*/}
                    <Route path="/" element={<MainLayout/>}>
                        <Route index element={<MainPage/>}/>
                        <Route path="tariffs" element={<TariffsPage/>}/>
                        <Route path="about" element={<AboutPage/>}/>
                    </Route>

                {/*Panel*/}
                <Route path="/panel/" element={<AuthLayout/>}>
                    <Route path="signin" element={<SignInPage/>}/>
                    <Route path="signup" element={<SignUpPage/>}/>
                    <Route path="recovery"/>
                </Route>
            </Routes>
        </UserProvider>
        )
};

export default App;
