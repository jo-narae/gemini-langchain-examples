import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure the API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# Initialize the model (gemini-2.0-flash)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def main():
    print("=" * 50)
    print("Gemini 2.0 Flash Example")
    print("=" * 50)

    # Example 1: Simple text generation
    print("\n[Example 1] Simple Text Generation")
    prompt1 = "Python에서 가장 중요한 3가지 특징을 간단히 설명해주세요."
    response1 = model.generate_content(prompt1)
    print(f"Prompt: {prompt1}")
    print(f"Response: {response1.text}\n")

    # Example 2: Code generation
    print("[Example 2] Code Generation")
    prompt2 = "Python으로 피보나치 수열을 구하는 함수를 작성해주세요."
    response2 = model.generate_content(prompt2)
    print(f"Prompt: {prompt2}")
    print(f"Response: {response2.text}\n")

    # Example 3: Interactive chat
    print("[Example 3] Interactive Chat")
    chat = model.start_chat(history=[])

    message1 = "안녕하세요! 당신의 이름은 무엇인가요?"
    response = chat.send_message(message1)
    print(f"User: {message1}")
    print(f"AI: {response.text}\n")

    message2 = "머신러닝과 딥러닝의 차이점을 간단히 설명해주세요."
    response = chat.send_message(message2)
    print(f"User: {message2}")
    print(f"AI: {response.text}\n")

    # Example 4: Streaming response
    print("[Example 4] Streaming Response")
    prompt3 = "AI의 미래에 대해 짧게 이야기해주세요."
    print(f"Prompt: {prompt3}")
    print("Response (streaming): ", end="")
    response3 = model.generate_content(prompt3, stream=True)
    for chunk in response3:
        print(chunk.text, end="", flush=True)
    print("\n")

    print("=" * 50)
    print("All examples completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()
