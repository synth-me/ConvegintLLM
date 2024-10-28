from library.Pricing import Pricing
import json 
from openai import OpenAI
import re
import difflib 

class CallAI:
    """Class to handle AI-related operations."""

    def __init__(self, path: str = "./database/token.json"):
        """Initializes the CallAI class with the path to the token file and sets up the OpenAI client.
        
        Args:
            path (str): Path to the token file. Defaults to "./token.json".
        """
        self.temperature = 0.2
        self.language    = "English"
        
        with open(path) as json_token:
            content = json.loads(json_token.read())["token"]
            self.client = OpenAI(api_key=content)
        
        self.pricing = Pricing()

    def change_language(self,lang: str = "English") -> None:
        """Simply choose a differente database, for different language documentation
        
        Args:
            lang (str): The new language according to the database pattern
        
        """
        self.language = lang 

    def renderPrompt(self) -> str:
        """Reads and returns the content of the database.js file.

        Returns:
            str: The content of the database.js file.
        """
        with open(f'./database/database_{self.language}.js') as database:
            return database.read()

    def extract_code(self, markdown_string: str) -> str:
        """Extracts code from a markdown string.

        Args:
            markdown_string (str): The markdown string containing the code.

        Returns:
            str: The extracted code, or the original string if no code is found.
        """
        code_match = re.search(r'```(?:\w*\n)?([\s\S]*?)```', markdown_string)
        if code_match:
            return code_match.group(1).strip()
        return markdown_string
    
    def diff_(self, str1: str, str2: str) -> tuple:
        """
        Find and return the parts of the two strings after their longest common substring.

        Args:
            str1 (str): The first input string.
            str2 (str): The second input string.

        Returns:
            tuple: A tuple containing the second parts of str1 and str2 after splitting them by the longest common substring.
                If no common substring is found, returns a tuple of empty strings ("", "").
        """
        # Find the longest common substring
        matcher = difflib.SequenceMatcher(None, str1, str2)
        match = matcher.find_longest_match(0, len(str1), 0, len(str2))

        if match.size == 0:
            return "", ""  # No common substring found

        common_substring = str1[match.a:match.a + match.size]

        # Split the strings based on the common substring
        parts1 = str1.split(common_substring, 1)
        parts2 = str2.split(common_substring, 1)

        # Keep the second part
        second_part1 = parts1[1] if len(parts1) > 1 else ""
        second_part2 = parts2[1] if len(parts2) > 1 else ""

        return second_part1, second_part2

    def ngram_jaccard_similarity(self,s1:str , s2: str, n:int =2) -> float:
        """
        Calculate the Jaccard similarity between two strings based on n-grams.

        Args:
            s1 (str): The first input string.
            s2 (str): The second input string.
            n (int, optional): The length of the n-grams to be used. Defaults to 2.

        Returns:
            float: The Jaccard similarity between the two input strings.
        """
        ngrams = lambda s: set(zip(*[s[i:] for i in range(n)]))
        s1_ngrams = ngrams(s1)
        s2_ngrams = ngrams(s2)
        return len(s1_ngrams & s2_ngrams) / len(s1_ngrams | s2_ngrams)

    def find_most_similar(self, input_line:str) -> str:
        """
        Find the most similar line to the input line from a file using n-gram Jaccard similarity.

        Args:
            input_line (str): The input string to compare.

        Returns:
            str: The most similar line found in the file.
        """
        # Read the lines from the file
        with open("./database/methods.js", 'r') as file:
            lines = file.readlines()
        
        lines = [line.strip() for line in lines]
        
        max_similarity = -1
        most_similar_line = None
        for line in lines:
            similarity = self.ngram_jaccard_similarity(input_line, line)
            if similarity > max_similarity:
                max_similarity = similarity
                most_similar_line = line
        
        return most_similar_line


    def complete_code(self, prompt: str) -> str:
        """Generates code completion using OpenAI's GPT model.

        Args:
            prompt (str): The prompt to generate the code completion for.

        Returns:
            str: The completed code extracted from the model's response.
        """
        _, content = self.diff_(prompt,self.find_most_similar(prompt))
        return content

    def generate_code(self, prompt: str) -> str:
        """Generates code completion using OpenAI's GPT model.

        Args:
            prompt (str): The prompt to generate the code completion for.

        Returns:
            str: The completed code extracted from the model's response.
        """
        code_prompt = self.renderPrompt()
        full_prompt = [
            {"role": "system", "content": code_prompt},
            {"role": "user", "content": prompt}
        ]
        completion = self.client.chat.completions.create(
            model="gpt-4o", 
            messages=full_prompt,
            temperature = self.temperature
        )
        
        content = completion.choices[0].message.content
        self.pricing.calculate_prompt_cost_wrapper(full_prompt)
        self.pricing.calculate_completion_cost_wrapper(completion)
        return self.extract_code(content)
    
    def generate_documentation(self, prompt: str) -> str:
        """Generates code documentation using OpenAI's GPT model.

        Args:
            prompt (str): The code to generate the documentation for.

        Returns:
            str: The generated documentation
        """ 
        code_prompt = """
        You're a generator of JSDocs documentation , 
        generate the correspondent documentation for the following code and solely
        the documentation, no additional text. 
        """
        full_prompt = [
            {"role": "system", "content": code_prompt},
            {"role": "user", "content": prompt}
        ]
        completion = self.client.chat.completions.create(
            model="gpt-4o", 
            messages=full_prompt,
            temperature=self.temperature
        )
        
        content = completion.choices[0].message.content
        self.pricing.calculate_prompt_cost_wrapper(full_prompt)
        self.pricing.calculate_completion_cost_wrapper(completion)
        
        return content 
