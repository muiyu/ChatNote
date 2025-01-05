import axios from 'axios';

export const uploadMarkdownFile = async (file, question) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('question', question);

  try {
    const response = await axios.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error('Error uploading file:', error);
    throw error;
  }
};