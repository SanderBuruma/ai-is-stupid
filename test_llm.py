#!/usr/bin/env python3
"""
Test LLM prompts to demonstrate issues with 1st and 2nd order inferences.
"""
import os
import re
import google.generativeai as genai
from collections import Counter


def load_api_key():
    """Load Gemini API key from environment or .env file."""
    # Try to load from .env if exists
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

    return os.getenv('GEMINI_API_KEY'), os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')


def extract_words(text):
    """Extract words from CSV response, filtering out common CSV artifacts."""
    # Remove common CSV separators and split into words
    words = re.findall(r'[a-zA-Z]+', text)
    return words


def analyze_response(response_text):
    """Analyze response for words containing 'a' and 'e'."""
    words = extract_words(response_text)

    words_with_a = []
    words_with_e = []

    for word in words:
        word_lower = word.lower()
        has_a = 'a' in word_lower
        has_e = 'e' in word_lower

        if has_a:
            words_with_a.append(word)
        if has_e:
            words_with_e.append(word)

    return {
        'total_words': len(words),
        'words_with_a': words_with_a,
        'words_with_e': words_with_e,
        'count_with_a': len(words_with_a),
        'count_with_e': len(words_with_e),
        'all_words': words
    }


def run_prompt_test(model, prompt, num_tests=100):
    """Run the prompt multiple times and collect results."""
    results = []

    print(f"Testing prompt {num_tests} times...")
    print(f"Prompt: {prompt}")
    print("=" * 80)

    for i in range(num_tests):
        try:
            response = model.generate_content(prompt)
            response_text = response.text

            analysis = analyze_response(response_text)
            analysis['response_text'] = response_text
            analysis['test_number'] = i + 1
            results.append(analysis)

            print(f"\nTest {i + 1}/{num_tests}")
            print("-" * 80)
            print(f"Response:\n{response_text}")
            print(f"\nAnalysis:")
            print(f"  Total words: {analysis['total_words']}")
            print(f"  Words with 'a': {analysis['count_with_a']}")
            print(f"  Words with 'e': {analysis['count_with_e']} (VIOLATIONS - should be 0)")

            if analysis['words_with_e']:
                print(f"  VIOLATIONS: {', '.join(analysis['words_with_e'])}")

        except Exception as e:
            print(f"\nTest {i + 1}/{num_tests} - ERROR: {str(e)}")
            results.append({
                'test_number': i + 1,
                'error': str(e)
            })

    return results


def print_summary(results):
    """Print summary statistics."""
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    successful_tests = [r for r in results if 'error' not in r]
    failed_tests = [r for r in results if 'error' in r]

    print(f"Total tests: {len(results)}")
    print(f"Successful: {len(successful_tests)}")
    print(f"Failed: {len(failed_tests)}")

    if successful_tests:
        total_violations = sum(r['count_with_e'] for r in successful_tests)
        avg_violations = total_violations / len(successful_tests)
        tests_with_violations = sum(1 for r in successful_tests if r['count_with_e'] > 0)

        print(f"\nViolation Statistics (words with 'e' when prompt said 'without the letter e'):")
        print(f"  Tests with violations: {tests_with_violations}/{len(successful_tests)} ({100*tests_with_violations/len(successful_tests):.1f}%)")
        print(f"  Total violations: {total_violations}")
        print(f"  Average violations per test: {avg_violations:.2f}")

        # Count most common violation words
        all_violations = []
        for r in successful_tests:
            all_violations.extend([w.lower() for w in r['words_with_e']])

        if all_violations:
            violation_counts = Counter(all_violations)
            print(f"\nMost common violation words:")
            for word, count in violation_counts.most_common(10):
                print(f"    {word}: {count} times")


def main():
    """Main entry point."""
    api_key, model_name = load_api_key()

    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment or .env file")
        return

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    prompt = "Give me 50 7 letter nouns with the letter A anywhere in the word and without the letter E in CSV format one line. Do NOT respond with ANYTHING else but the CSV line. Do not respond with anything that has the letter E."

    results = run_prompt_test(model, prompt, num_tests=10)
    print_summary(results)


if __name__ == '__main__':
    main()
