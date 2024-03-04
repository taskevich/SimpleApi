import React from 'react';

const SignUpPage = () => {
    return(
        <form>
            <input type="text" name="login"/>
            <input type="email" name="email"/>
            <input type="tel" name="phone"/>
            <input type="text" name="password"/>
            <input type="checkbox" name="notifications"/>
            <button>
                Создать аккаунт
            </button>
        </form>
    )
};

export default SignUpPage;