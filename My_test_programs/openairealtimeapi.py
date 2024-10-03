import asyncio
import json
import os
import base64
from dotenv import load_dotenv
import websockets
from pydub import AudioSegment
import io
import numpy as np

# Load environment variables
load_dotenv()

OPENAI_API_KEY =os.environ["OPENAI_API_KEY"]

if not OPENAI_API_KEY:
    print('Please set your OPENAI_API_KEY in the .env file')
    exit(1)

URL = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-10-01"


def save_to_file(data, filename, mode='w'):
    """
    Save data to a file.

    :param data: The data to save. Can be string, bytes, or any serializable object.
    :param filename: The name of the file to save to.
    :param mode: The file mode. 'w' for text, 'wb' for binary.
    """
    try:
        if mode == 'w':
            with open(filename, mode, encoding='utf-8') as file:
                if isinstance(data, str):
                    file.write(data)
                else:
                    json.dump(data, file, indent=2)
        elif mode == 'wb':
            with open(filename, mode) as file:
                file.write(data)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")


async def send_event(websocket, event):
    await websocket.send(json.dumps(event))


def audio_to_item_create_event(audio_bytes: bytes) -> dict:
    # Load the audio file from the byte stream
    audio = AudioSegment.from_file(io.BytesIO(audio_bytes))

    # Resample to 24kHz mono pcm16
    pcm_audio = audio.set_frame_rate(24000).set_channels(1).set_sample_width(2).raw_data

    # Encode to base64 string
    pcm_base64 = base64.b64encode(pcm_audio).decode()

    event = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [{
                "type": "input_audio",
                "audio": pcm_base64
            }]
        }
    }
    return event


async def handle_function_call(websocket, function_call):
    print('Function call:', function_call)
    # Here you would typically call the actual function and send the result back
    function_result_event = {
        "type": "conversation.item.create",
        "item": {
            "type": "function_call_output",
            "function_call_id": function_call["id"],
            "output": json.dumps({
                "temperature": 22,
                "unit": "celsius",
                "description": "Partly cloudy"
            })
        }
    }
    await send_event(websocket, function_result_event)

    # Request another response after sending function result
    response_create_event = {
        "type": "response.create",
        "response": {
            "modalities": ["text", "audio"],
        }
    }
    await send_event(websocket, response_create_event)


async def handle_audio_response(audio_base64):
    audio_bytes = base64.b64decode(audio_base64)
    print(f"Received audio response of {len(audio_bytes)} bytes")
    # Save the audio response to a file
    save_to_file(audio_bytes, "assistant_response.wav", mode='wb')


def float_to_16bit_pcm(float32_array):
    """Convert Float32Array to 16-bit PCM."""
    int16_array = (float32_array * 32767).astype(np.int16)
    return int16_array.tobytes()


def base64_encode_audio(float32_array):
    """Convert Float32Array to base64-encoded PCM16 data."""
    pcm_data = float_to_16bit_pcm(float32_array)
    return base64.b64encode(pcm_data).decode()


async def stream_audio_files(websocket, file_paths):
    """Stream audio files to the API."""
    for file_path in file_paths:
        audio = AudioSegment.from_file(file_path)
        audio = audio.set_frame_rate(24000).set_channels(1).set_sample_width(2)

        # Convert to numpy array
        samples = np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0

        # Encode and send
        base64_chunk = base64_encode_audio(samples)
        await send_event(websocket, {
            "type": "input_audio_buffer.append",
            "audio": base64_chunk
        })

    # Commit the audio buffer
    await send_event(websocket, {"type": "input_audio_buffer.commit"})


async def main():
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "OpenAI-Beta": "realtime=v1",
    }

    async with websockets.connect(URL, extra_headers=headers) as websocket:
        print('Connected to OpenAI Realtime API')

        # Set up the session
        session_update_event = {
            "type": "session.update",
            "session": {
                "instructions": "You are a helpful AI assistant. Respond concisely.",
                "tools": [
                    {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "unit": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"]
                                },
                            },
                            "required": ["location", "unit"],
                        },
                    },
                ],
                "voice": "alloy",
                "turn_detection": "server_vad",
            },
        }
        await send_event(websocket, session_update_event)

        # Send a user text message
        user_message_event = {
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "What's the weather like in New York?"
                    }
                ]
            }
        }
        await send_event(websocket, user_message_event)

        # Stream audio files
        audio_files = [
            './path/to/sample1.wav',
            './path/to/sample2.wav',
            './path/to/sample3.wav'
        ]
        await stream_audio_files(websocket, audio_files)

        # Request a response
        response_create_event = {
            "type": "response.create",
            "response": {
                "modalities": ["text", "audio"],
            }
        }
        await send_event(websocket, response_create_event)

        try:
            while True:
                message = await websocket.recv()
                event = json.loads(message)
                print('Received event:', event['type'])

                if event['type'] == 'conversation.item.created':
                    if event['item']['type'] == 'message' and event['item']['role'] == 'assistant':
                        for content in event['item']['content']:
                            if content['type'] == 'text':
                                print('Assistant:', content['text'])
                                save_to_file(content['text'], "assistant_response.txt")
                            elif content['type'] == 'audio':
                                await handle_audio_response(content['audio'])
                    elif event['item']['type'] == 'function_call':
                        await handle_function_call(websocket, event['item']['function_call'])
                elif event['type'] == 'error':
                    print('Error:', event['error'])
                    save_to_file(event['error'], "error_log.json")
                elif event['type'] == 'input_audio_buffer.speech_started':
                    print('Speech started')
                elif event['type'] == 'input_audio_buffer.speech_stopped':
                    print('Speech stopped')
                elif event['type'] == 'input_audio_buffer.committed':
                    print('Audio buffer committed')

        except websockets.exceptions.ConnectionClosed:
            print('Disconnected from OpenAI Realtime API')


if __name__ == "__main__":
    asyncio.run(main())