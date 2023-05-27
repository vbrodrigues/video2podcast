import openai
import tiktoken


def extract_keypoints(text_path: str, context: str, output_path: str = None, max_tokens=100) -> str:

    with open(text_path, 'r') as f:
        text = f.read()
    
    print('Summarizing text...')
    context_intro = f'Given that you are an expert on {context}, extract the important keypoints from the following text:\n\n'
    
    enc = tiktoken.get_encoding("cl100k_base")
    context_tokens = enc.encode(context_intro)
    tokens = enc.encode(text)
    valid_tokens = tokens[:4097-len(context_tokens)-max_tokens]
    valid_text = enc.decode(valid_tokens)

    response = openai.Completion.create(
        model='text-davinci-003', 
        prompt=context_intro + valid_text, 
        max_tokens=max_tokens,
    )

    output_path = output_path if output_path is not None else 'data/keypoints/keypoints.txt'
    with open(output_path, 'w') as f:
        f.write(response['choices'][0]['text'])
    
    return response['choices'][0]['text']


def create_chat(text_path: str, context: str, person1: str = 'Liz', person2: str = 'John', output_path: str = None, max_tokens=100) -> str:
    
    with open(text_path, 'r') as f:
        text = f.read()

    print(f'Creating chat between {person1} and {person2}')
    response = openai.Completion.create(
        model='text-davinci-003', 
        prompt=f'Given that you are an expert on {context}, create a conversation between two people name {person1} and {person2} where each talk about one of the following keypoints:\n\n'+text, 
        max_tokens=max_tokens,
    )

    output_path = output_path if output_path is not None else 'data/chats/chat.txt'
    with open(output_path, 'w') as f:
        f.write(response['choices'][0]['text'])

    return response['choices'][0]['text']