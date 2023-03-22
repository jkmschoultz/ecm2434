import React from 'react';
import classes from "./main.css";
import GreenNavbar from "../../components/greenNavbar";
import LoginPopup from "../../components/loginPopup";
import Logo from "../../assets/Logo.png";


const Main = () => {
    return (
        <>
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"/>
          <GreenNavbar />
          <div className="container-fluid p-0">          
            <div className="background-image"></div>
            <div className="overlay">
              <h1>H 2 GO</h1>
              <p>Keep Hydrated by refilling you water bottle.</p>  
              {/*<img src={Logo} alt="Logo" className="logo" />*/}
            </div>
            <LoginPopup />
          </div>

          <div class="information-section">
  <div class="container">
    <div class="row">
      <div class="col-sm-6">
        <h2>Welcome to H2gO!!</h2>
        <p>We are here to help you find water fountains on campus!
           Find maps of the buildings closest to you that show you where all the water fountains are. While you're here, 
           why not sign up with us to compete in our sustainability game! </p>
        <p>Who is the most knowledgeable about sustainability in the Forum?
          Who's filled up the most bottles in the Business School?
          Find out with our leaderboards and register to join in the competition yourself!</p>
        <p>Who we are</p>
        <p>We are a group of Computer Science students at University of Exeter who want to help students be sustainable on campus.
           We made this app to promote students and teachers to use refillable water bottles that they can fill at water fountains, 
          and prevent people from buying those ridiculous one-time use plastic bottles!</p>
        <p>For us, every time a water bottle is filled at a fountain is one less plastic bottle being bought. 
          With this website, we track how many plastic bottles we've avoided being bought by people using our app! And while we're at it, we want users of our app to be educated about sustainability.
           Try answering our quizzes to find out how much you know yourself!</p>
      </div>
      <div class="col-sm-6">
        <img src={Logo} alt="Information Image" class="img-responsive" />
      </div>
 
      </div>
    </div>
       </div>
        
        </>
      );
}

export default Main;
