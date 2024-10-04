
import tiktoken

def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name="cl100k_base")
    num_tokens = len(encoding.encode(string, disallowed_special=()))
    return num_tokens

# Example usage:
# num_tokens = num_tokens_from_string("Sample text")
