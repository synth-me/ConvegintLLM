import json

class Token:
    """Class to handle token saving and loading."""

    def __init__(self, path: str = "./database/token.json"):
        """Initializes the Token class with the path to the token file.

        Args:
            path (str): Path to the token file. Defaults to "./database/token.json".
        """
        self.path = path

    def save_token(self, token: str) -> None:
        """Saves the token to a JSON file.

        Args:
            token (str): The token to be saved.
        """
        with open(self.path, "w") as json_token:
            json.dump({"token": token}, json_token)

    def load_token(self) -> str:
        """Loads the token from a JSON file.

        Returns:
            str: The loaded token.
        """
        with open(self.path) as json_token:
            return json.loads(json_token.read())["token"]