import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import React, {useEffect, useState} from "react";
import Cookies from 'js-cookie';

function App() {
    const [csrfToken, setCsrfToken] = useState('');

    function setCookie(name, value, days, path, secure) {
        let expires = "";

        // Set expiration date if specified
        if (days) {
            const date = new Date();
            date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000)); // Convert days to milliseconds
            expires = "; expires=" + date.toUTCString();
        }

        // Construct cookie string
        let cookieString = `${name}=${encodeURIComponent(value)}${expires}; path=${path || '/'};`;

        // Add SameSite and Secure attributes if specified
        if (secure) {
            cookieString += " Secure; SameSite=None;";
        } else {
            cookieString += " SameSite=Lax;"; // Default SameSite attribute
        }

        // Set the cookie
        document.cookie = cookieString;
    }

    useEffect(() => {
        if (!Cookies.get("csrftoken")){
        axios.get('http://127.0.0.1:8000/csrf-token', {withCredentials: true})
            .then(response => {
                console.log(response.data);
            });
        }
    }, []);

    const handleSubmit = async (event) => {
        event.preventDefault();
        console.log(document.cookie)
        try {
            const response = await axios.post('http://127.0.0.1:8000/auth/register', {
                email: "test1@test.com",
                first_name: "Kassim",
                last_name: "Chaudhry",
                username: "kassim1_c222",
                password: "test",
            }, {
                xsrfCookieName: 'csrftoken',
                xsrfHeaderName: 'X-CSRFToken',
                headers: {
                    "X-CSRFToken": Cookies.get("csrftoken"),
                    'Content-Type': 'application/json',
                },
                withCredentials: true,
            });
            // const response = await axios.get('http://127.0.0.1:8000/auth/loggedin',{
            //     xsrfCookieName: 'csrftoken',
            //     xsrfHeaderName: 'X-CSRFToken',
            //     headers: {
            //         "X-CSRFToken": Cookies.get("csrftoken"),
            //         'Content-Type': 'application/json',
            //     },
            //     withCredentials: true,
            // });
            console.log(response.data);
        } catch (error) {
            console.error('There was an error!', error);
        }
    };


    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
                <p>
                    Edit <code>src/App.js</code> and save to reload.
                </p>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a>
            </header>

            <button type="submit" onClick={(event) => handleSubmit(event)}>Submit</button>
        </div>
    );
}

export default App;
