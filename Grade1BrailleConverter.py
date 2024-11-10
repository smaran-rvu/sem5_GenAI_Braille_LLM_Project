class Grade1BrailleConverter:
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

        # Numbers (preceded by number sign ⠼)
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
            '[': '⠨⠣',    # opening square bracket
            ']': '⠨⠜',    # closing square bracket
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
            '/': '⠸⠌',    # forward slash
            '…': '⠲⠲⠲',   # ellipsis
        }

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
                    result.append('⠼')  # Number sign
                    in_number = True
                result.append(self.numbers[text[i]])
                i += 1
                continue
            else:
                in_number = False

            # Check for uppercase
            if text[i].isupper():
                result.append('⠠')  # Capital sign

            # Check for punctuation
            if text[i] in self.punctuation:
                result.append(self.punctuation[text[i]])
                i += 1
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
    converter = Grade1BrailleConverter()
    
    # Test cases
    test_cases = [
        "Hello World!",
        "CAPITAL LETTERS",
        "Numbers 123",
        "Special @#$%",
        "Mixed Case Text",
        "Punctuation: !?.,",
        "Temperature is 25°C",
        "Email: test@example.com",
        "Price: $99.99",
        "A-Z: abcdefghijklmnopqrstuvwxyz"
    ]
    
    print("Grade 1 Braille Conversion Tests:")
    print("-" * 50)
    for test in test_cases:
        braille = converter.to_braille(test)
        print(f"Original: {test}")
        print(f"Braille:  {braille}")
        print("-" * 50)