from typing import Union
from pathlib import Path
from random import choice
from json import load
from time import time

from rich import print
from rich import box
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text

pathToWords: Path = Path('./words.json')

class Profile:
    def __init__(self) -> None:
        pass


class Word:
    def __init__(self, word: str) -> None:
        self.word: str = word
        self.diff: int = len(word)

        self.letters: list[str] = self.__generateLetters()

    def __log(self):
        print(self.word)

    def __generateLetters(self) -> list[str]:
        letters: list[str] = []
        for l in self.word:
            letters.append(l)

        return letters

    def value(self) -> str:
        return self.word
    
    

def load_words() -> dict[str, int]:
    with open(pathToWords, 'r') as j:
        return load(j)

def generate_word_list(diff: int, length: int) -> list[Word]:
    wordList: list[Word] = []
    words: list = list(load_words().keys())
    
    while len(wordList) < length:
        word = choice(words)
        
        if len(word) <= diff:
            wordList.append(Word(word))
            
    return wordList

def generate_panel(word_list: list[Word]) -> Panel:
    words: list[str] = [n.value() for n in word_list]
    words_converted: Text = Text(' '.join(words), justify='center')
    
    panel: Panel = Panel(words_converted, title='TYPY', box=box.ROUNDED)
    
    return panel
    

def main():
    diff: Union[str, int] = Prompt.ask("difficulty", default=10, show_default=True)
    word_list: list[Word] = generate_word_list(int(diff), 5)

    print(generate_panel(word_list))

    start = time()        
    results: Union[str, int] = Prompt.ask(">")
    end = time()
    speed = round((end - start), 2)

    results_to_list: list[str] = results.split(' ')
    
    if results_to_list == [n.value() for n in word_list]:
        print('correct')
    else:
        print('wrong')

    print(speed)

    
if __name__ == '__main__':
    main()