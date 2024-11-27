from Matching import Matching

lowercase_cyrillic_letters = [chr(i) for i in range(0x0430, 0x044F + 1)]
capital_cyrillic_letters = [chr(i) for i in range(0x0410, 0x042F + 1)]
lowercase_english_letters = [chr(i) for i in range(0x0061, 0x007A + 1)]
capital_english_letters = [chr(i) for i in range(0x0041, 0x005A + 1)]
digits = [chr(i) for i in range(0x0030, 0x0039 + 1)]

class Term:
    def __init__(self, letter):
        if letter in lowercase_cyrillic_letters:
            self.letters = lowercase_cyrillic_letters
            self.symbol = "Tc"
            return
        if letter in capital_cyrillic_letters:
            self.letters = capital_cyrillic_letters
            self.symbol = "TC"
            return
        if letter in lowercase_english_letters:
            self.letters = lowercase_english_letters
            self.symbol = "Te"
            return
        if letter in capital_english_letters:
            self.letters = capital_english_letters
            self.symbol = "TE"
            return
        if letter in digits:
            self.letters = digits
            self.symbol = "Td"
            return
        
        self.letters = [letter]
        self.symbol = f"T{letter}"
    
    def isEqual(self, other):
        return self.symbol == other.symbol


class Struc:
    def __init__(self, a : str):
        self.terms = []
        
        for letter in a:
            candidateTerm = Term(letter)
            
            if len(self.terms) == 0 or not self.terms[-1].isEqual(candidateTerm):
                self.terms.append(candidateTerm)
    
        self.symbol = ""
        for t in self.terms:
            self.symbol += t.symbol
    
    def isEqual(self, other):
        return ''.join(self.terms) == ''.join(other.terms)

class Transformation:
    def __init__(self, m : Matching):
        self.m = m
        self.lhs = Struc(m.a)
        self.rhs = Struc(m.b)
        self.symbol = f"{self.lhs.symbol} -> {self.rhs.symbol}"
    
    def isEqualStrucs(self, other):
        return self.symbol == other.symbol
    
    def print(self):
        print(f"{self.m.a} -> {self.m.b}")
        
        