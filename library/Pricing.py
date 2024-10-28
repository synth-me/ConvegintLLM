import tokencost 
import sqlite3 
from datetime import datetime, timedelta 

class Pricing:
    """This class can calculate the price for each request, which will be very useful for the experiments"""
    def __init__(self):
        self.model = "gpt-4-0613"
        self.db_path = "./logs/log.db"
        self._initialize_db()
        self.tokencost = tokencost 
        return None 

    def _initialize_db(self):
        """Initialize the database and create the table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY,
                datetime TEXT,
                cost FLOAT,
                tokens INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def calculate_prompt_cost_wrapper(self,prompt: dict) -> float:
        """Calculate the amount of $ that the entire prompt took 
        
        Args:
            prompt (dict): The whole data structure that the model takes in

        Returns:
            int: The value in $ that you just spent

        """
        cost = float(self.tokencost.calculate_prompt_cost(prompt,self.model))
        counting = self.tokencost.count_message_tokens(prompt, self.model)
        self.log(cost,counting)
        return cost 

    def calculate_completion_cost_wrapper(self, completion: dict) -> float:
        """Calculate the amount of $ that the entire completion took 
        
        Args:
            prompt (str): The whole data structure that the model takes in

        Returns:
            int: The value in $ that you just spent

        """
        cost = float(self.tokencost.calculate_completion_cost(completion.choices[0].message.content, self.model))
        counting = completion.usage.completion_tokens 
        self.log(cost,counting)
        return cost

    def sum_costs_last_24h(self) -> float:
        """Sum the costs from the last 24 hours.

        Returns:
            float: The total cost from the last 24 hours.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            now = datetime.now()
            past_24h = now - timedelta(hours=24)
            past_24h_iso = past_24h.isoformat()

            cursor.execute('''
                SELECT SUM(cost) FROM requests
                WHERE datetime >= ?
            ''', (past_24h_iso,))

            result = cursor.fetchone()[0]
            total_cost = float(result) if result is not None else 0.0

            conn.close()
            return total_cost
        except Exception as e:
            print(f"An error occurred while querying: {e}")
            return 0.0

    def log(self,cost: float, tokens: int) -> bool:

        """Log the request details into the SQLite database
        
        Args:
            cost (float): The cost of the request
            tokens (int): The amount of tokens used in the request

        Returns:
            bool: True if logging was successful, False otherwise
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().isoformat()
        cursor.execute('''
            INSERT INTO requests (datetime, cost, tokens)
            VALUES (?, ?, ?)
        ''', (timestamp, cost, tokens))
        conn.commit()
        conn.close()
        return True

# eof 