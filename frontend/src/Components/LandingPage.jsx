import React from 'react'
import '../styles/LandingPage.css'
import Header from './Header'

const LandingPage = ({loggedIn}) => {

    const handleLogin = () => {
        if (loggedIn){
            window.location.href = './dashboard'
        } else {
            window.location.href = './login';
        }
    }

  return (
    <>  
    <Header/>
    <div className='landing-page-container'>
        <div className="landing-page-content-container">
            <div className='landing-page-content std-box'>
                <h1>
                    Draw.
                </h1>
                <h3>
                    Real-time collaborative white board
                </h3>
            </div>
        </div>

        <div className="landing-page-cta std-box">
            <button className='std-box' onClick={handleLogin}><h1>Get Started</h1></button>
        </div>
    </div>
    </>
     )
}

export default LandingPage
