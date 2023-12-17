
import sys
import json
import logging
from text2emotion import get_emotion
import emoji
    
def process_text(text):
    emotions = get_emotion(text)
    return {
        "happy": emotions["Happy"],
        "sad": emotions["Sad"],
        "angry": emotions["Angry"],
        "surprise": emotions["Surprise"],
        "fear": emotions["Fear"]
    }

def remove_emojis(text):
    return emoji.get_emoji_regexp().sub(u'', text)

def send_message(message):
    # Get the emotion with the highest probability
    max_emotion = max(message["result"], key=lambda k: message["result"][k])
    text_without_emojis = remove_emojis(max_emotion)
    message_length = len(text_without_emojis).to_bytes(4, byteorder='little')
    sys.stdout.buffer.write(message_length)
    sys.stdout.buffer.write(text_without_emojis.encode('utf-8'))
    sys.stdout.buffer.flush()
    
def main():
    while True:
        try:
            message_length_bytes = sys.stdin.buffer.read(4)
            if not message_length_bytes:
                sys.exit(1)

            message_length = int.from_bytes(message_length_bytes, byteorder='little')

            remaining_bytes = message_length - 4
            message_bytes = message_length_bytes + sys.stdin.buffer.read(remaining_bytes)
            message_str = message_bytes.decode('utf-8', errors='replace')
            message_dict = json.loads(message_str)
            text = message_dict.get("text")
            if message_dict.get("action") == "analyzeText":
                text = message_dict.get("text")
                result = process_text(text)

                result_message = {"action": "emotionResult", "result": result}
                send_message(result_message)

        except json.JSONDecodeError as e:
            logging.error("JSON Decode Error(script.py): %s", e)
            print("JSON Decode Error(script.py):", e)

        except Exception as e:
            logging.error("Error(script.py): %s", e)
            print("Error(script.py):", e)

if __name__ == "__main__":
    main()
