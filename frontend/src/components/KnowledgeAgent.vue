<template>
  <div>
    <h1>Knowledge Agent</h1>
    <input type="file" accept=".md" @change="handleFileChange" />
    <input type="text" v-model="question" placeholder="Enter your question" />
    <button @click="handleSubmit">Upload and Process</button>
    <div v-if="response">
      <h2>Response:</h2>
      <pre>{{ response }}</pre>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue';
import { uploadMarkdownFile } from '@/services/api';

export default {
  setup() {
    const file = ref(null);
    const question = ref('');
    const response = ref('');

    const handleFileChange = (event) => {
      file.value = event.target.files[0];
    };

    const handleSubmit = async () => {
      if (file.value && question.value) {
        try {
          const result = await uploadMarkdownFile(file.value, question.value);
          response.value = result.response;
        } catch (error) {
          console.error('Error:', error);
        }
      }
    };

    return {
      file,
      question,
      response,
      handleFileChange,
      handleSubmit,
    };
  },
};
</script>