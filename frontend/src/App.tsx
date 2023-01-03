import React from 'react';
import logo from './logo.svg';
import './App.css';
import PlayersLogin from './components/players/PlayersLogin';
import { Route, Routes } from 'react-router-dom';
import Home from './components/home/Home';
import PlayersCreate from './components/players/PlayersCreate';

function App() {
  return (
   <Routes>
    <Route path="/login" element={<PlayersLogin />}/>
    <Route path="/register" element= {<PlayersCreate />}/>
    <Route path="/" element={<Home />}/>
   </Routes>
  );
}

export default App;
