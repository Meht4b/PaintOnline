import { useState } from 'react'
import '../styles/Login.css'
import { useEffect } from 'react';
import APIEndpoint from '../APIEndpoint';

function Login({propLogin, propError,setLoggedIn,callBack}) {

    

    const [Login, setLogin] = useState(propLogin);
    const [Error, setError] = useState(propError);
    const [userCreated, setUserCreated] = useState(0);

    const [name, setName] = useState("");
    const [password, setPassword] = useState("");


    const handleSubmit = async (event) => {

        event.preventDefault();
        const user = { name, password };

        if (Login == 0) {
            const url =APIEndpoint+ "/create_user";
            const options = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user),
            };

            const response = await fetch(url, options);
            if (response.ok) {
                setName("");
                setPassword("");
                setLogin(1);
                setError(0);
                setUserCreated(1);
            } else {
                console.log(response.json().error)
                setError(1);
            }
        }

        if (Login == 1) {
            const url = APIEndpoint + "/check_password"
            const options = {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(user),
            };

            

            const response = await fetch(url, options);
            const data = await response.json();

            if (response.ok) {
                console.log(data);
                sessionStorage.setItem("token", data.access_token);
                sessionStorage.setItem("loggedIn", 1);
                sessionStorage.setItem("user", name);
                setLoggedIn(1);
                callBack();
            }else if(response.status == 401 || response.status == 403) {

                sessionStorage.removeItem("token");
                sessionStorage.setItem("loggedIn", 0);
                sessionStorage.removeItem("user");
            
            } else {
                setError(1);
                setName("");
                setPassword("");
                console.log(data.error)
            }
        }

    }

    useEffect(() => {
        if (userCreated === 1) {
            const timer = setTimeout(() => {
                setUserCreated(0);
            }, 5000);
            return () => clearTimeout(timer);
        }
    }, [userCreated]);

    useEffect(() => {
        if (Error === 1) {
            const timer = setTimeout(() => {
                setError(0);
            }, 5000);
            return () => clearTimeout(timer);
        }
    }, [Error]);


    return (
        <>

        <form className="login-container" onSubmit={handleSubmit}>
            {Login ? <h1>Login</h1> : <h1>Register</h1>}
            <div className="input-group">
                <label htmlFor="username"><h3>User Name :</h3></label>
                <input 
                    type="text" 
                    id="username"
                    name="username"
                    autoComplete="off" autoCapitalize="off"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
            </div>
            <div className="input-group">
                <label htmlFor="password"><h3>Password :</h3></label>
                <input 
                    type="password"
                    id="password"
                    name="password"
                    autoComplete="off" autoCapitalize="off"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </div>


            {Login ?
                <button type="submit" className='login-submit'><h2>Login</h2></button>:
                <button type="submit" className='login-submit register-submit'><h2>Register </h2></button>
            }

                        {Login == 1 && (
                <button type='button' className='register-link' onClick={() => 
                    {setLogin(0)
                    setError(0)}}>
                    <h3>New? Register here</h3>
                </button>
            )}
        </form>

        {Error == 1 && Login == 1 && (
            <div className='login-error'><h3>Password or username is incorrect</h3></div>
        )}

        {Error == 1 && Login == 0 && (
            <div className='login-error'><h3>Username already exists</h3></div>
        )}

        {
            userCreated == 1 && (
                <div className='register-success'><h3>User created successfully! You can now login.</h3></div>
            )
        }

          </>
    )
}

export default Login
