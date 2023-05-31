import openai
import tiktoken


def extract_keypoints(text_path: str, context: str, output_path: str = None, max_tokens=100) -> str:

    with open(text_path, 'r') as f:
        text = f.read()
    
    print('Summarizing text...')
    context_intro = f'Given that you are an expert on {context}, extract the important keypoints from the following text (be as extensive as you want, as many keypoints as possible):\n\n'
    
    enc = tiktoken.get_encoding("cl100k_base")
    context_tokens = enc.encode(context_intro)
    tokens = enc.encode(text)
    valid_tokens = tokens[:4096-len(context_tokens)-max_tokens]
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
        prompt=f"Given that you are an expert on {context}, create an extensive, lengthy and laid-back conversation between two people: {person1} (main host) and {person2} (co-host). They know each other for years and constantly make fun of each other. They are the hosts to a podcast and the podcast's name you have to create yourself. The conversation must end with the hosts closing the podcast. They are talking about the following topics:\n\n"+text, 
        max_tokens=max_tokens,
    )

    output_path = output_path if output_path is not None else 'data/chats/chat.txt'
    with open(output_path, 'w') as f:
        f.write(response['choices'][0]['text'])

    return response['choices'][0]['text']