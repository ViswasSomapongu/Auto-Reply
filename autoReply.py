import pyautogui
import pyperclip
import time
import google.generativeai as genai
import re

api_key = "YOUR_API_KEY"  # Replace with your actual API key

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="Provide your instructions for the model to generate responses as per your requirements."

)

chat_session = model.start_chat(
    history=[
        
    ]
)


def format_chat_history(raw_chat):
    #  raw chat history copied from WhatsApp looks like
    # [7:10 PM] Alex: Hey there!
    # [7:11 PM] Sarah: Hi Alex!
    # [7:12 PM] Alex: How's your day going?
    # [7:12 PM] Sarah: It's going well, thanks! How about you?
    # [7:13 PM] Alex: Pretty good, just catching up on some work.
    # [7:15 PM] Sarah: That sounds busy! Anything exciting happening?

    message_pattern = r"\[(.*?)\] (.*?): (.*)"
    formatted_chat = []
    for match in re.finditer(message_pattern, raw_chat):
        timestamp, speaker, message = match.groups()
        formatted_chat.append(f"{speaker}: {message}")
    if formatted_chat:
        last_message = formatted_chat[-1].split(":", 1)
        last_speaker = last_message[0] if len(last_message) > 1 else None
        return last_speaker, "\n".join(formatted_chat)
    return None, ""


# Get current mouse position
# import pyautogui
# while True:
#     position = pyautogui.position()
#     print(position)


# Move the mouse cursor to the  position of the WhatsApp on Taskbar (Adjust these coordinates to match the position of WhatsApp on your taskbar)
pyautogui.moveTo(1165, 1160)
pyautogui.click()

while True:
    try:
        time.sleep(2)
        
        # Select and copy the entire chat history on WhatsApp
        pyautogui.moveTo(600, 215)
        pyautogui.dragTo(1800, 1040, duration=2)
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)
        pyautogui.click(1822, 1000)

        # Retrieve the copied chat history from clipboard
        raw_chat_history = pyperclip.paste()
        # print("Raw Chat History:")
        # print(raw_chat_history)
        last_speaker, formatted_chat_history = format_chat_history(raw_chat_history)
        # print("Formatted Chat History:")
        # print(formatted_chat_history)
        # print("Last Speaker:")
        # print(last_speaker)
 

        if last_speaker and last_speaker != "YourName": # Repace with your name
            response = chat_session.send_message(formatted_chat_history)
            response_text = response.text

            # print("Response Text:")
            # print(response_text)

            # Copy the generated response to clipboard
            pyperclip.copy(response_text)

            # Click on the WhatsApp chat input field and paste the generated response
            pyautogui.moveTo(755, 1080)
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')

            time.sleep(3)

    except Exception as e:
        print(f"An error occurred: {e}")
        break
