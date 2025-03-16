import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import Editor from './pages/Editor';
import { ThemeProvider } from '@mui/material/styles';
import theme from './theme';

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <Router>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/editor/:id" element={<Editor />} />
          </Routes>
      </Router>
    </ThemeProvider>
  );
};

export default App;