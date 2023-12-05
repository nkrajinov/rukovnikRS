import { initializeApp } from 'firebase/app';
import { getAuth } from "firebase/auth";
import { getFirestore } from 'firebase/firestore/lite';


const firebaseConfig = {
  apiKey: "AIzaSyC3HBbbC2y9OFncuqKzRlAYO4J1lHl7Dm8",
  authDomain: "rukovnik-cdc5a.firebaseapp.com",
  projectId: "rukovnik-cdc5a",
  storageBucket: "rukovnik-cdc5a.appspot.com",
  messagingSenderId: "72936066238",
  appId: "1:72936066238:web:9ca8b708373a486218a2ef"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);
const auth = getAuth(app);

export default {
  app,
  db,
  auth
}