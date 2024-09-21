import json

class Conversation:
    def __init__(self, max_history_length=10, summarization_threshold=15):
        """
        Initialize the ConversationManager with options for max history length and when to start summarizing.
        :param max_history_length: The maximum number of messages to keep in full detail.
        :param summarization_threshold: The number of messages after which summarization of old messages will occur.
        """
        self.history = []  # Holds the conversation history as a list of message dictionaries
        self.max_history_length = max_history_length
        self.summarization_threshold = summarization_threshold

    def add_message(self, message):
        """
        Add a new message object to the conversation history.
        :param message: The Message object to add.
        """

        self.history.append(message)

        # Trim conversation history if it's too long
        self.trim_history()

    def trim_history(self):
        """
        Trim the conversation history to the maximum length. Summarize older messages if the history grows too large.
        """
        if len(self.history) > self.summarization_threshold:
            self.summarize_older_messages()
        elif len(self.history) > self.max_history_length:
            # Keep the first and last few messages, discard the middle ones
            self.history = self.history[-self.max_history_length:]

    def summarize_older_messages(self):
        """
        Summarize the earlier part of the conversation to keep within the token limit.
        """
        # Summarize older messages to condense the history
        summary = "Summary of previous conversation: The user and assistant discussed various topics."
        # Keep system message, summary, and last few messages
        self.history = [self.history[0], {"role": "assistant", "content": summary}] + self.history[
                                                                                      -self.max_history_length:]

    def get_history(self):
        """
        Retrieve the entire conversation history.
        :return: List of dictionaries representing the conversation history.
        """
        return self.history

    def get_serialized_history(self):
        """
        Get the conversation history serialized as a JSON string.
        :return: A JSON string representing the conversation history.
        """
        return json.dumps(self.history)

    def load_history_from_json(self, json_data):
        """
        Load conversation history from a JSON string.
        :param json_data: A JSON string representing the conversation history.
        """
        self.history = json.loads(json_data)

    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.history = []


