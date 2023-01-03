import React from 'react';
import logo from './logo.svg';
import './App.css';
import PlayersLogin from './players/PlayersLogin';
import { Route, Routes } from 'react-router-dom';

function App() {
  return (
   <Routes>
    <Route path="/login" element={<PlayersLogin />}/>
    <Route path="/" element={<PlayersLogin />}/>
   </Routes>
  );
}

export default App;
