import React from 'react';
import Header from './Header';
import Footer from './Footer';
import { Container } from '@mui/material';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <Container>
            <Header />
            <main>{children}</main>
            <Footer />
        </Container>
    );
};

export default Layout;