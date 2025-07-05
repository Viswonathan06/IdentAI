// Import useState and useEffect hooks
import React, { useState, useEffect } from 'react';
import { Container, Form, Button, Alert } from 'react-bootstrap';
import axios from 'axios';

const Login = ({ history }) => {
  const [loginMethod, setLoginMethod] = useState('');
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [recording, setRecording] = useState(false);
  const [audioStream, setAudioStream] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const [audioUrl, setAudioUrl] = useState('');

  useEffect(() => {
    if (recording) {
      // Reset audioChunks when starting recording again
      setAudioChunks([]);

      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          setAudioStream(stream);
          const mediaRecorder = new MediaRecorder(stream);
          mediaRecorder.ondataavailable = (e) => {
            setAudioChunks(prevChunks => [...prevChunks, e.data]);
          };
          mediaRecorder.start();
        })
        .catch(error => {
          console.error('Error accessing microphone:', error);
          setError('Error accessing microphone. Please check your permissions.');
        });
    } else {
      if (audioStream) {
        audioStream.getTracks().forEach(track => track.stop());
        setAudioStream(null);
      }
    }
  }, [recording]);

  const handleLogin = async () => {
    // Login logic...
    if (loginMethod === 'idPass') {
      try {
        const data = {
          'userId': userId,
          'password': password
        }
        const response = await axios.post('http://127.0.0.1:5000/login_with_password', data);
        if (response.data.status === 'success') {
          localStorage.setItem('isLoggedIn', 'true');
          history.push('/dashboard');
        } else {
          setError('Invalid ID or password');
        }
      } catch (error) {
        setError('Error logging in');
      }
    } else if (loginMethod === 'liveRecording') {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      const formData = new FormData();
      formData.append('audioFile', audioBlob);
      formData.append('userId', userId);

      try {
        const response = await axios.post('http://127.0.0.1:5000/login_with_audio', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        if (response.data.status === 'success') {
          localStorage.setItem('isLoggedIn', 'true');
          history.push('/dashboard');
        } else {
          setError('Authentication failed');
        }
      } catch (error) {
        setError('Error logging in');
      }
    }
  };

  const handlePlayAudio = () => {
    // If there are audio chunks, create a Blob and set the audio URL
    if (audioChunks.length > 0) {
      const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
      setAudioUrl(URL.createObjectURL(audioBlob));
    } else {
      // If there are no audio chunks, clear the audio URL
      setAudioUrl('');
    }
  };

  return (
    <Container className="d-flex justify-content-center align-items-center vh-100">
      <div>
        <Form>
          <Form.Check
            type="radio"
            id="idPass"
            label="Login with ID/Password"
            checked={loginMethod === 'idPass'}
            onChange={() => setLoginMethod('idPass')}
          />
          <Form.Check
            type="radio"
            id="liveRecording"
            label="Login with Live Recording"
            checked={loginMethod === 'liveRecording'}
            onChange={() => setLoginMethod('liveRecording')}
          />
          {loginMethod === 'idPass' && (
            <>
              <Form.Group controlId="userId">
                <Form.Label>User ID</Form.Label>
                <Form.Control type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
              </Form.Group>
              <Form.Group controlId="password">
                <Form.Label>Password</Form.Label>
                <Form.Control type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
              </Form.Group>
            </>
          )}
          {loginMethod === 'liveRecording' && (
            <Form.Group controlId="userIdLiveRecording">
              <Form.Label>User ID</Form.Label>
              <Form.Control type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
            </Form.Group>
          )}

          {/* Start/Stop recording button */}
          {loginMethod === 'liveRecording' && audioUrl ==='' && !recording && (
            <Button variant="primary" onClick={() => setRecording(true)}>
              Start Recording
            </Button>
          )}

          {loginMethod === 'liveRecording' && recording && (
            <Button variant="danger" onClick={() => setRecording(false)}>
              Stop Recording
            </Button>
          )}

          {/* Play recorded audio button */}
          {audioChunks.length > 0 && (
            <Button variant="info" onClick={handlePlayAudio} className="mt-2">
              Play Recorded Audio
            </Button>
          )}

          <Button variant="primary" onClick={handleLogin}>
            Login
          </Button>
          {error && <Alert variant="danger">{error}</Alert>}
        </Form>

        {/* Audio player */}
        {audioUrl && (
          <audio controls className="mt-3">
            <source src={audioUrl} type="audio/wav" />
            Your browser does not support the audio element.
          </audio>
        )}
      </div>
    </Container>
  );
};

export default Login;
