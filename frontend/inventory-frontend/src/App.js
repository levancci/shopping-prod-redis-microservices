import logo from './logo.svg';
import './App.css';
import { Products } from './components/Products';
import { Orders } from './components/Orders';

import { ProductCreate } from './components/ProductCreate';
import {BrowserRouter, Route, Routes} from 'react-router-dom'

function App() {
  return <BrowserRouter> 
  <Routes>
      <Route path="/" element={<Products/>}/>
      <Route path="/create" element={<ProductCreate/>}/>
      <Route path="/orders" element={<Orders/>}/>
    </Routes>
  </BrowserRouter>;
}

export default App;
