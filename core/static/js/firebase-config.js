// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-analytics.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDl9eRg6gZ6KvNHI62NTG27omy7NotS4U4",
  authDomain: "college-connect-69dd1.firebaseapp.com",
  projectId: "college-connect-69dd1",
  storageBucket: "college-connect-69dd1.firebasestorage.app",
  messagingSenderId: "1099282874349",
  appId: "1:1099282874349:web:8f1f4b5146159eb71f71e4",
  measurementId: "G-ND2Z1EEL18"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

console.log("Firebase initialized successfully!");

// You can export these if you plan to use them in other JS files
export { app, analytics };
