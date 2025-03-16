import React from 'react';
import { Container, Box, Button, Typography, Popover, Modal, Backdrop } from '@mui/material';
import VerticalLinearStepper from '../components/Stepper';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 600,
    height: 'auto',
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  }; 

const Home: React.FC = () => {

    const [anchorEl, setAnchorEl] = React.useState<HTMLButtonElement | null>(null);
    const [open, setOpen] = React.useState(false);

    const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
        setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
    };
  
   // const open = Boolean(anchorEl);
    // const id = open ? 'simple-popover' : undefined;
    return (
        <Container>
            <Box sx={{ 
                bgcolor: '#cfe8fc', 
                height: '50vh', 
                width: '50ww', 
                display: "flex",
                flexDirection: "row",
                alignItems: "flex-start", // Aligns children to the start (left)
                padding: "16px",
                position: 'relative', 
                borderRadius: "10px", 
                columnGap: "16px", // Add spacing between items in a flex container
                filter: open ? 'blur(5px)' : 'none', // Add blur effect when popover is open
                transition: 'filter 0.3s ease' // Smooth transition for blur effect
            }}>
                <Typography 
                    sx={{position:'absolute', top: "16px", left:"16px"}} 
                    variant="h5" 
                    color="primary"
                >
                    Video
                </Typography>
                <Button 
                    sx={{ 
                        marginTop: "64px" // Add space below the Typography
                    }} 
                    variant="contained" 
                    color="primary"
                    onClick={handleClick}
                >
                   Idea(Prompt)    
                </Button>
                <Button 
                    sx={{ 
                        marginTop: "64px" // Add space below the Typography
                    }} 
                    variant="contained" 
                    color="primary"
                >
                   Option 2   
                </Button>
            </Box>
            <Modal
                open={open}
                onClose={handleClose}
                closeAfterTransition
                slots={{ backdrop: Backdrop }}
                slotProps={{
                    backdrop: {
                        sx: { backgroundColor: 'rgba(0, 0, 0, 0.5)' }
                    }
                }}
            >
                <Box sx={style}>
                    <VerticalLinearStepper />
                </Box>
            </Modal>
        </Container>
    );
};

export default Home;