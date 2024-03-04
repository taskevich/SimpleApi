import React from 'react';

const SignInPage = () => {
    return (
        <form>
            <input type="text" name="login"/>
            <input type="text" name="password"/>
            <button>
                Войти
            </button>
        </form>
    )
};

export default SignInPage;