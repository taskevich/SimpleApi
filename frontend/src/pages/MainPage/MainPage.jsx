import React from 'react';
import Logo from "../../ui/Logotype/Logo";
import  "./style.scss"
import NavButton from "../../ui/NavButton/NavButton";


const MainPage = () => {
    return (
        <section className="project flex">
            <h1>BACKEND из коробки</h1>
            <Logo/>
            <div className="flex gap">
                <NavButton>Get Started</NavButton>
                <NavButton>Docs</NavButton>
            </div>
            <div className="flex content">
                <div className="img">

                </div>
                <div className="text">
                    <h2>Lorem ipsum dolor sit amet</h2>
                    <h3>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</h3>
                    <p>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. In et odio eget  metus sagittis maximus. Mauris efficitur sit amet metus quis congue.  Sed auctor in odio at varius. Pellentesque et tempus quam. Fusce vitae  gravida magna. Proin malesuada, dolor pretium eleifend dictum, dolor dui  facilisis leo, ut imperdiet massa lectus sit amet ante. Donec sed velit  vitae eros viverra sollicitudin. Etiam sit amet ex tempus, consequat  sem malesuada, facilisis orci. Nullam faucibus laoreet turpis, eget  sodales tellus imperdiet sed. Sed dignissim mollis sem. Quisque ultrices  ornare imperdiet.
                    </p>
                </div>
            </div>
        </section>
    )
};

export default MainPage;