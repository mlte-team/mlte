const express = require('express');
const bodyParser = require('body-parser');
const { Configuration, OpenAIApi } = require('openai');
require('dotenv').config();

const app = express();
const port = 3000;

app.use(bodyParser.json());

const openai = new OpenAIApi(new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
}));

app.post('/api/get-recommendations', async (req, res) => {
  try {
    const { projectDescription, currentStrategies, challenges } = req.body;

    const prompt = `
      Project Description: ${projectDescription}
      Current Strategies: ${currentStrategies}
      Challenges: ${challenges}
      
      Based on the above information, provide personalized recommendations for optimizing machine learning model latency.
    `;

    const completion = await openai.createChatCompletion({
      model: 'gpt-4',
      messages: [{ role: 'user', content: prompt }],
    });

    const recommendations = completion.data.choices[0].message.content;
    res.json({ recommendations });
  } catch (error) {
    console.error('Error fetching recommendations:', error);
    res.status(500).json({ error: 'Failed to fetch recommendations' });
  }
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
