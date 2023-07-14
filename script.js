document.getElementById('question-form').addEventListener('submit', async function(event) {
  event.preventDefault();
  
  const questionInput = document.getElementById('question-input');
  const responseContainer = document.getElementById('response-container');
  
  const question = questionInput.value;
  
  // Send the question to the backend for processing
  const response = await fetch('/query', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ question })
  });
  
  // Retrieve the response from the backend
  const { response: answer } = await response.json();
  
  // Display the response on the web page
  responseContainer.innerHTML = `<p><b>Response:</b> ${answer}</p>`;
  
  // Reset the input field
  questionInput.value = '';
});
