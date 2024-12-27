import React, { useState } from 'react';
import axios from 'axios';
import { useDropzone } from 'react-dropzone';

function App() {
  const [file, setFile] = useState(null);
  
  const onDrop = (acceptedFiles) => {
    setFile(acceptedFiles[0]);
  };

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  const uploadFile = async () => {
    if (!file) {
      alert('No file selected');
      return;
    }
    
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post('http://localhost:8000/api/upload/', formData);
    alert('File uploaded: ' + response.data.url);
  };

  return (
    <div>
      <h1>Cloud File Manager</h1>
      <div {...getRootProps()} style={{ border: '2px dashed #ccc', padding: '20px', width: '300px', textAlign: 'center' }}>
        <input {...getInputProps()} />
        <p>Drag and drop a file here, or click to select one</p>
      </div>
      <button onClick={uploadFile}>Upload</button>
    </div>
  );
}

export default App;
