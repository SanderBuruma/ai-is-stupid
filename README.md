# AI is Stupid

A demonstration project that tests LLM capabilities with simple constraint-based prompts to highlight failures in 1st and 2nd order inferences.

## What Does This Do?

This script tests how well Large Language Models can follow simple constraints by repeatedly asking them to generate words that:
- Contain the letter 'A'
- Do NOT contain the letter 'E'

The prompt specifically asks for "50 7-letter nouns with the letter A anywhere in the word and without the letter E" and explicitly instructs the model not to include any words with 'E'.

## Why?

Despite the explicit instructions, LLMs frequently fail this simple task by including words that contain the letter 'E'. This demonstrates fundamental issues with:
- **1st order inference**: Understanding the basic constraint (no letter E)
- **2nd order inference**: Validating their own output against the stated constraint

## Setup

1. Clone the repository:
```bash
git clone https://github.com/SanderBuruma/ai-is-stupid.git
cd ai-is-stupid
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Gemini API credentials:
```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

## Usage

Run the test script:
```bash
python3 test_llm.py
```

The script will:
1. Run the prompt 10 times (configurable in the script)
2. Analyze each response for constraint violations
3. Count and highlight words containing 'E'
4. Display a summary showing violation statistics

## Example Output

```
Test 1/10
--------------------------------------------------------------------------------
Response:
banana, papaya, ...

Analysis:
  Total words: 50
  Words with 'a': 50
  Words with 'e': 12 (VIOLATIONS - should be 0)
  VIOLATIONS: apple, orange, grape, ...
```

## Results

After all tests complete, you'll see summary statistics including:
- Percentage of tests with violations
- Total number of violations across all tests
- Average violations per test
- Most commonly violated words

## Current Model

Testing: **Gemini 2.5 Flash**

## License

MIT
