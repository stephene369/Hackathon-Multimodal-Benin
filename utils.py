
import re

def find_keywords_regex(text, keywords):
    """
    Search for keywords in a string using regular expressions to match whole words.

    Parameters:
        text (str): The text to search within.
        keywords (list of str): Keywords to look for.

    Returns:
        list: A list of keywords found in the text.
    """
    found_keywords = []
    text = text.lower()
    for keyword in keywords:
        # Use word boundaries to ensure the keyword is not part of a larger word
        if re.search(r'\b' + re.escape(keyword.lower()) + r'\b', text):
            found_keywords.append(keyword)
    return found_keywords

# Example usage
text = "Here is a sample text that includes words like python, function, and list."
keywords = ["ami wɔ", "amiwo", "array"]
found = find_keywords_regex(text, keywords)
print("Keywords found:", found)


