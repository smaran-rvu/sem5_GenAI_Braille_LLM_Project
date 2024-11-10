import json
import re

class Grade2BrailleConverter:
    def __init__(self):
        # Single characters
        self.alphabet = {
            'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑',
            'f': '⠋', 'g': '⠛', 'h': '⠓', 'i': '⠊', 'j': '⠚',
            'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕',
            'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞',
            'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽',
            'z': '⠵', ' ': '⠀'
        }

        # Numbers and their corresponding braille letters (a-j)
        self.numbers = {
            '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
            '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚'
        }

       # Special characters
        self.special_chars = {
            '@': '⠈⠁',    # at sign
            '#': '⠸⠹',    # hash/number
            '$': '⠈⠎',    # dollar
            '%': '⠨⠴',    # percent
            '&': '⠈⠯',    # ampersand
            '*': '⠐⠔',    # asterisk
            '+': '⠐⠖',    # plus
            '=': '⠐⠶',    # equals
            '_': '⠨⠤',    # underscore
            '|': '⠸⠳',    # vertical bar
            '~': '⠈⠔',    # tilde
            '^': '⠘⠢',    # caret
            '<': '⠈⠣',    # less than
            '>': '⠈⠜',    # greater than
            '[': '⠨⠣',   # opening square bracket
            ']': '⠨⠜',   # closing square bracket
            '•': '⠸⠲',    # bullet
            '©': '⠘⠉',    # copyright
            '®': '⠘⠗',    # registered trademark
            '™': '⠘⠞',    # trademark
            '€': '⠈⠑',    # euro
            '£': '⠈⠇',    # pound
            '¥': '⠈⠽',    # yen
            '°': '⠘⠚',    # degree
            '±': '⠐⠖⠤',   # plus-minus
            '²': '⠘⠃',    # superscript 2
            '¹': '⠘⠁',    # superscript 1
            '⁰': '⠘⠚',    # superscript 0
            '³': '⠘⠉',    # superscript 3
            '⁴': '⠘⠙',    # superscript 4
            '⁵': '⠘⠑',    # superscript 5
            '⁶': '⠘⠋',    # superscript 6
            '⁷': '⠘⠛',    # superscript 7
            '⁸': '⠘⠓',    # superscript 8
            '⁹': '⠘⠊',    # superscript 9
            '₁': '⠰⠁',    # subscript 1
            '₂': '⠰⠃',    # subscript 2
            '₃': '⠰⠉',    # subscript 3
            '₄': '⠰⠙',    # subscript 4
            '₅': '⠰⠑',    # subscript 5
            '₆': '⠰⠋',    # subscript 6
            '₇': '⠰⠛',    # subscript 7
            '₈': '⠰⠓',    # subscript 8
            '₉': '⠰⠊',    # subscript 9
            '₀': '⠰⠚',    # subscript 0
        }

        # Punctuation
        self.punctuation = {
            '.': '⠲',      # period
            ',': '⠂',      # comma
            ';': '⠆',      # semicolon
            ':': '⠒',      # colon
            '!': '⠖',      # exclamation
            '?': '⠦',      # question
            '"': '⠦',      # quote
            '(': '⠐⠣',    # opening parenthesis
            ')': '⠐⠜',    # closing parenthesis
            "'": '⠄',      # apostrophe
            '-': '⠤',      # hyphen
            '/': '⠸⠌',     # forward slash
            '…': '⠲⠲⠲',   # ellipsis
        }

        # Common whole-word contractions (same as before)
        self.whole_word_contractions = {
            'but': '⠃', 'can': '⠉', 'do': '⠙', 'every': '⠑',
            'from': '⠋', 'go': '⠛', 'have': '⠓', 'just': '⠚',
            'knowledge': '⠅', 'like': '⠇', 'more': '⠍', 'not': '⠝',
            'people': '⠏', 'quite': '⠟', 'rather': '⠗', 'so': '⠎',
            'that': '⠞', 'us': '⠥', 'very': '⠧', 'will': '⠺',
            'it': '⠭', 'you': '⠽', 'as': '⠵', 'and': '⠯',
            'for': '⠿', 'of': '⠷', 'the': '⠮', 'with': '⠾',
            'in': '⠔', 'was': '⠴', 'were': '⠶'
        }

        # Common letter group contractions (same as before)
        self.letter_group_contractions = {
            'ch': '⠡', 'gh': '⠣', 'sh': '⠩', 'th': '⠹', 'wh': '⠱',
            'ed': '⠫', 'er': '⠻', 'ou': '⠳', 'ow': '⠪', 'ar': '⠜',
            'ing': '⠬', 'tion': '⠰⠝', 'ness': '⠰⠎', 'ment': '⠰⠞'
        }

    def _is_whole_word(self, text, start, word):
        """Check if the word at the given position is a whole word."""
        end = start + len(word)
        if end > len(text):
            return False
        
        # Check if the word matches at this position
        if text[start:end].lower() != word:
            return False
        
        # Check boundaries
        before_ok = start == 0 or not text[start-1].isalpha()
        after_ok = end == len(text) or not text[end].isalpha()
        
        return before_ok and after_ok

    def to_braille(self, text):
        if not text:
            return ""

        result = []
        i = 0
        in_number = False
        
        while i < len(text):
            # Check for special characters first
            if text[i] in self.special_chars:
                result.append(self.special_chars[text[i]])
                i += 1
                in_number = False
                continue

            # Check for numbers
            if text[i].isdigit():
                if not in_number:
                    result.append('⠼')
                    in_number = True
                result.append(self.numbers[text[i]])
                i += 1
                continue
            else:
                in_number = False

            # Check for uppercase
            if text[i].isupper():
                result.append('⠠')

            # Check for punctuation
            if text[i] in self.punctuation:
                result.append(self.punctuation[text[i]])
                i += 1
                continue

            # Check for whole word contractions
            word_found = False
            for word, contraction in self.whole_word_contractions.items():
                if self._is_whole_word(text, i, word):
                    if i == 0 or text[i-1] == ' ':
                        result.append(contraction)
                        i += len(word)
                        word_found = True
                        break
            if word_found:
                continue

            # Check for letter group contractions
            group_found = False
            for group, contraction in self.letter_group_contractions.items():
                if i + len(group) <= len(text) and text[i:i+len(group)].lower() == group:
                    result.append(contraction)
                    i += len(group)
                    group_found = True
                    break
            if group_found:
                continue

            # Handle regular letters
            char = text[i].lower()
            if char in self.alphabet:
                result.append(self.alphabet[char])
            else:
                result.append(char)  # Keep unrecognized characters as-is
            i += 1

        return ''.join(result)

# Example usage
if __name__ == "__main__":
    converter = Grade2BrailleConverter()
    
    # Test cases including special characters
    test_cases = [
        "The quick brown fox jumps over the lazy dog",
        "Email me at: test@example.com",
        "Price: $99.99 (50% off!)",
        "Temperature: 23°C",
        "x = y + z * 2",
        "Copyright © 2024",
        "{Python} [Code] <HTML>",
        "~!@#$%^&*()_+",
        "Hello... World!",
        "https://www.example.com",
    ]
    
    print("Grade 2 Braille Conversion Tests:")
    print("-" * 50)
    for test in test_cases:
        braille = converter.to_braille(test)
        print(f"Original: {test}")
        print(f"Braille:  {braille}")
        print("-" * 50)