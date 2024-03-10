import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyAwGvzXbpV6jiPBf1qVeiGQ5ujt3dUI0Ac",
    authDomain: "project-news-972eb.firebaseapp.com",
    projectId: "project-news-972eb",
    storageBucket: "project-news-972eb.appspot.com",
    messagingSenderId: "641658097205",
    appId: "1:641658097205:web:404f167ae84d7aa2a1eb7c",
    measurementId: "G-L678TPC2J0"
  };

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

const googleSignInBtn = document.getElementById('l');

const provider = new GoogleAuthProvider();
googleSignInBtn.addEventListener('click', () => {
  signInWithPopup(auth, provider)
    .then((result) => {
      const user = result.user;
      location.replace('/index')
});
});