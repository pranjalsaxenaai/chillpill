import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, Card, CardContent, Box, Paper } from '@mui/material';
import { useParams } from 'react-router-dom';

// Mock data for scenes
interface Scene {
  id: number;
  name: string;
  description: string;
}

const Editor: React.FC = () => {
    const { id } = useParams<{ id: string }>();
    const [scenes, setScenes] = useState<Scene[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [selectedScene, setSelectedScene] = useState<Scene | null>(null);
    
    // Mock API call
    useEffect(() => {
        const fetchScenes = async () => {
            setLoading(true);
            const mockApiCall = new Promise<Scene[]>((resolve) => {
                setTimeout(() => {
                    resolve([
                        { id: 1, name: 'Opening Scene', description: 'Introduction to the main character' },
                        { id: 2, name: 'Conflict Scene', description: 'Main problem is introduced' },
                        { id: 3, name: 'Resolution', description: 'Problem gets resolved' },
                        { id: 4, name: 'Ending', description: 'Final scene showing conclusion' },
                    ]);
                }, 1500);
            });

            try {
                const data = await mockApiCall;
                setScenes(data);
                if (data.length > 0) setSelectedScene(data[0]);
            } catch (error) {
                console.error('Error fetching scenes:', error);
            } finally {
                setLoading(false);
            }
        };

        if (id) {
            fetchScenes();
        }
    }, [id]);

    return (
        <Container maxWidth="xl" sx={{ mt: 4 }}>
            <Typography variant="h4" gutterBottom>
                Video Editor - Project ID: {id}
            </Typography>
            
            <Grid container spacing={2}>
                {/* First Grid - Scene List */}
                <Grid item xs={4}>
                    <Paper elevation={3} sx={{ p: 2, height: '70vh', overflow: 'auto' }}>
                        <Typography variant="h6" gutterBottom>Scenes</Typography>
                        {loading ? (
                            <Typography>Loading scenes...</Typography>
                        ) : (
                            scenes.map((scene) => (
                                <Card 
                                    key={scene.id}
                                    sx={{ 
                                        mb: 2, 
                                        cursor: 'pointer',
                                        bgcolor: selectedScene?.id === scene.id ? 'primary.light' : 'inherit'
                                    }}
                                    onClick={() => setSelectedScene(scene)}
                                >
                                    <CardContent>
                                        <Typography variant="subtitle1">{scene.name}</Typography>
                                        <Typography variant="body2" color="text.secondary">
                                            {scene.description}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            ))
                        )}
                    </Paper>
                </Grid>
                
                {/* Second Grid - Video Player */}
                <Grid item xs={4}>
                    <Paper elevation={3} sx={{ p: 2, height: '70vh' }}>
                        <Typography variant="h6" gutterBottom>Video Preview</Typography>
                        <Box 
                            sx={{ 
                                width: '100%',
                                height: 'calc(70vh - 80px)',
                                bgcolor: 'black',
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'center'
                            }}
                        >
                            {/* Placeholder for video player */}
                            <Typography color="white">
                                {selectedScene 
                                    ? `Playing: ${selectedScene.name}`
                                    : 'No scene selected'
                                }
                            </Typography>
                            {/* In a real app, you would add a video player component here */}
                            {/* Example: <ReactPlayer url="https://example.com/video" width="100%" height="100%" /> */}
                        </Box>
                    </Paper>
                </Grid>
                
                {/* Third Grid - Properties/Settings */}
                <Grid item xs={4}>
                    <Paper elevation={3} sx={{ p: 2, height: '70vh', overflow: 'auto' }}>
                        <Typography variant="h6" gutterBottom>Properties</Typography>
                        {selectedScene && (
                            <Box>
                                <Typography variant="subtitle1">
                                    Scene: {selectedScene.name}
                                </Typography>
                                <Typography variant="body1" paragraph>
                                    {selectedScene.description}
                                </Typography>
                                {/* Add more properties and controls here */}
                            </Box>
                        )}
                    </Paper>
                </Grid>
            </Grid>
        </Container>
    );
};

export default Editor;