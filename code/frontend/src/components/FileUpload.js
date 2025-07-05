import React, { useState } from 'react';
import { Alert, Button, Container, Form } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  
  const navigate = useNavigate();

  const handleLogout = () => {
    // Implement logout logic (e.g., clear authentication token)
    localStorage.setItem('isLoggedIn', 'false'); // Example: Clearing authentication status
    navigate('/');
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async () => {
    if (file) {
      const formData = new FormData();
      formData.append('audioFile', file);

      try {
        const response = await axios.post('url', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        if (response.data.status === 'success') {
          setAnalysisResult(response.data.analysis);
          setError(null);
        } else {
          setError('Analysis failed');
          setAnalysisResult(null);
        }
      } catch (error) {
        setError('Error uploading file');
        setAnalysisResult(null);
      }
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center vh-100">
      <div>
        <Form>
          <Form.Group controlId="formFile" className="mb-3">
            <Form.Control type="file" onChange={handleFileChange} accept=".mp3, .wav" />
          </Form.Group>
          <Button variant="primary" onClick={handleFileUpload}>
            Upload
          </Button>
        </Form>
        {error && <Alert variant="danger">{error}</Alert>}
        {analysisResult && (
          <div>
            <h2>Analysis Result</h2>
            <p>Detected Voice: {analysisResult.detectedVoice ? 'Yes' : 'No'}</p>
            <p>Voice Type: {analysisResult.voiceType}</p>
            <p>Confidence Score:</p>
            <ul>
              <li>AI Probability: {analysisResult.confidenceScore.aiProbability}%</li>
              <li>Human Probability: {analysisResult.confidenceScore.humanProbability}%</li>
            </ul>
            <p>Additional Info:</p>
            <ul>
              <li>Emotional Tone: {analysisResult.additionalInfo.emotionalTone}</li>
              <li>Background Noise Level: {analysisResult.additionalInfo.backgroundNoiseLevel}</li>
            </ul>
          </div>
        )}
      </div>
      <Button variant="danger" onClick={handleLogout}>
          Logout
        </Button>
    </Container>
  );
};

export default FileUpload;