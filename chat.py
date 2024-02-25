import openai
import tiktoken
import os


class Chat:

    def __init__(self, data_path: str):
        self.data_path = data_path
        self.__ensure_data_path_exists()

    def __ensure_data_path_exists(self):    
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

    def extract_keypoints(self, text_path: str, context: str, filename: str = 'keypoints.txt', max_tokens=100) -> str:
        output_path = os.path.join(self.data_path, filename)

        if not os.path.exists(output_path):
            with open(text_path, 'r') as f:
                text = f.read()
            
            print('Extracting keypoints...')
            context_intro = f'Given that you are an expert on {context}, extract the important keypoints from the following text (be as extensive as you want, as many keypoints as possible):\n\n'
            
            enc = tiktoken.get_encoding("cl100k_base")
            context_tokens = enc.encode(context_intro)
            tokens = enc.encode(text)

            for i in range(0, len(tokens), 4096):
                valid_tokens = tokens[i:i+4096-len(context_tokens)-max_tokens]
                valid_text = enc.decode(valid_tokens)

                response = openai.Completion.create(
                    model='gpt-3.5-turbo-instruct', 
                    prompt=context_intro + valid_text, 
                    max_tokens=max_tokens,
                )

                with open(output_path, 'a') as f:
                    f.write(response['choices'][0]['text'])

        return output_path


    def create_chat(self, text_path: str, context: str, person1: str = 'Liz', person2: str = 'John', filename: str = 'chat.txt', max_tokens=100) -> str:
        output_path = os.path.join(self.data_path, filename)
        
        if not os.path.exists(output_path):
            with open(text_path, 'r') as f:
                text = f.read()

            print(f'Creating chat between {person1} and {person2}')
            response = openai.Completion.create(
                model='gpt-3.5-turbo-instruct', 
                prompt=f"Given that you are an expert on {context}, create a laid-back podcast conversation between two people: {person1} (main host) and {person2} (co-host). They know each other for years and constantly make fun of each other. The podcast's name you have to create yourself. The conversation can be really long, with both talking like in a casual podcast and must end with the hosts closing the podcast. In the middle of the conversation, the host have to annouce an ad about a fictitional product, related to the topic, that you have to make up. Right before the end, they have to read messages from listeners and you have to make up the listeners names and messages. They are talking about the following topics:\n\n"+text, 
                max_tokens=max_tokens,
            )

            with open(output_path, 'w') as f:
                f.write(response['choices'][0]['text'])

        return output_path