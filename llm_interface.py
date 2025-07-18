"""
LLM interface for agent reasoning in the Virtual Economy Simulator.
Supports OpenAI API and mock (rule-based) fallback.
"""
import openai
import random
import config

# Safely get ChatCompletion and Completion if available
ChatCompletion = getattr(openai, 'ChatCompletion', None)
Completion = getattr(openai, 'Completion', None)

class LLMInterface:
    """
    Handles LLM-based decision making for agents.
    """
    def __init__(self, model=None, api_key=None, max_tokens=64, temperature=0.7):
        self.model = model or config.LLM_MODEL
        self.api_key = api_key or config.LLM_API_KEY
        self.max_tokens = max_tokens
        self.temperature = temperature
        if self.api_key:
            openai.api_key = self.api_key

    def get_action(self, prompt):
        if not self.api_key:
            return self.mock_action(prompt)
        try:
            # Try ChatCompletion (for chat models)
            if ChatCompletion is not None:
                response = ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
                answer = response['choices'][0]['message']['content'].strip().lower()
            elif Completion is not None:
                # Fallback for older OpenAI versions
                response = Completion.create(
                    model=self.model,
                    prompt=prompt,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                )
                answer = response['choices'][0]['text'].strip().lower()
            else:
                return self.mock_action(prompt)
            for option in ['buy', 'sell', 'save', 'invest']:
                if option in answer:
                    return option
            return 'hold'
        except Exception as e:
            print(f"LLM error: {e}")
            return self.mock_action(prompt)

    def mock_action(self, prompt):
        # Fallback: simple rule-based logic
        options = ['buy', 'sell', 'save', 'invest', 'hold']
        return random.choice(options) 