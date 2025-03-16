import React from 'react';
import { Box, Typography } from '@mui/material';

const Footer: React.FC = () => {
    return (
        <Box component="footer" sx={{ p: 2, textAlign: 'center', backgroundColor: '#f8f8f8' }}>
            <Typography variant="body2" color="textSecondary">
                © {new Date().getFullYear()} Your Company. All rights reserved.
            </Typography>
        </Box>
    );
};

export default Footer;