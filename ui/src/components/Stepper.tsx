import * as React from 'react';
import Box from '@mui/material/Box';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import StepContent from '@mui/material/StepContent';
import Button from '@mui/material/Button';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import TextField from '@mui/material/TextField/TextField';
import LinearProgress from '@mui/material/LinearProgress';

const steps = [
  {
    label: 'Prompt',
    },
  {
    label: 'Script',
  },
];

function VerticalLinearStepper() {
  const [activeStep, setActiveStep] = React.useState(0);
    const [isLoading, setIsLoading] = React.useState(false);
  const [formData, setFormData] = React.useState({
    prompt: '',
    script: '',
  });

  const handleNext = () => {
    if (activeStep == 0) {
        // fetch('https://api.example.com/generate-script', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({ prompt: formData.prompt })
        // })
    
    // Place holder to mimic API call
    setIsLoading(true);
    let p = new Promise<{data: string}>((resolve, reject) => {
        setTimeout(() => {
          resolve({data: 'test data'});
        }, 3000);
      });
        p.then(response => response)
        .then(data => {
            setFormData(prev => ({ ...prev, script: data.data }))
            setActiveStep((prevActiveStep) => prevActiveStep
            + 1);
            setIsLoading(false);
        })
        .catch(error => console.error('Error:', error));
    }
    else if (activeStep == 1) {
        // fetch('https://api.example.com/scenes', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json',
        //     },
        //     body: JSON.stringify({ script: formData.script })
        // })
        setIsLoading(true);
        let p = new Promise<{id: number}>((resolve, reject) => {
            setTimeout(() => {
              resolve({id : 123});
            }, 3000);
          });

        p.then(data => {
            // Navigate to Editor Component with the id
            setIsLoading(false);
            window.location.href = `/editor/${data.id}`;
            
            // Alternatively, if you're using React Router, you can use:
            // navigate(`/editor/${data.id}`);
        })
        .catch(error => console.error('Error:', error));
        // Do something
    }
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleReset = () => {
    setActiveStep(0);
  };

  const renderSteps = (step: number) => {
    switch (step) {
      case 0:
        return (
            <Box>
                <Typography sx={{fontWeight:500, fontSize: "0.875rem" }}>Put your Idea here(Max 50 words) </Typography>
                <TextField
                    id="outlined-multiline-static"
                    multiline
                    sx={{width: '100%'}}
                    value={formData.prompt}
                    rows={6}
                    onChange={(e) => setFormData({...formData, prompt: e.target.value})}
                    placeholder="Write your prompt here"
                    variant="outlined"
                />
          </Box>
        );
      case 1:
        return (
            <Box>
            <Typography sx={{fontWeight:500, fontSize: "0.875rem" }}>Generated Script </Typography>
            <TextField
                id="outlined-multiline-static"
                multiline
                sx={{width: '100%'}}
                value={formData.script}
                rows={6}
                onChange={(e) => setFormData({...formData, script: e.target.value})}
                placeholder="Script"
                variant="outlined"
            />
      </Box>
        );
      case 2:
        return (
          <Typography>{steps[2].label}</Typography>
        );          
      default:
        return 'Unknown step';} 
  }

  return (
    <Box>
    {isLoading && <LinearProgress />}
      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map((step, index) => (
          <Step key={step.label}>
            <StepLabel
              optional={
                index === steps.length - 1 ? (
                  <Typography variant="caption">Last step</Typography>
                ) : null
              }
            >
              {step.label}
            </StepLabel>
            <StepContent>
              {
                renderSteps(index)
              }
              <Box sx={{ mb: 2 }}>
                <Button
                  variant="contained"
                  onClick={handleNext}
                  sx={{ mt: 1, mr: 1 }}
                >
                  {index === steps.length - 1 ? 'Generate Scenes' : 'Generate Script'}
                </Button>
                <Button
                  disabled={index === 0}
                  onClick={handleBack}
                  sx={{ mt: 1, mr: 1 }}
                >
                  Back
                </Button>
              </Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>
      {activeStep === steps.length && (
        <Paper square elevation={0} sx={{ p: 3 }}>
          <Typography>All steps completed - you&apos;re finished</Typography>
          <Button onClick={handleReset} sx={{ mt: 1, mr: 1 }}>
            Reset
          </Button>
        </Paper>
      )}
    </Box>
  );
}


export default VerticalLinearStepper;

function then(arg0: (data: any) => void) {
    throw new Error('Function not implemented.');
}
