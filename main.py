from typing import Union

from pathlib import Path
from random import choice
from json import load, dump
from time import time
from os.path import exists

from rich import print
from rich import box
from rich.prompt import Prompt
from rich.padding import Padding
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from rich.layout import Layout


DEBUG: bool = True

pathToWords: Path = Path('./words.json')
if DEBUG:
    pathtoProfile: Path = Path('./profile.json')
else:
    pathtoProfile: Path = Path.home()


class Profile:
    def __init__(self) -> None:
        self.profile: dict = self.__load_profile()

    def __check_profile_exists(self) -> bool:
        return exists(pathtoProfile)

    def __load_profile(self) -> dict:
        mode: str = 'r' if self.__check_profile_exists() else 'w'

        with open(pathtoProfile, mode) as profile:
            p: dict = self.__profile_base()

            if mode == 'r':
                p = load(profile)
            else:
                dump(p, profile)

            return p
        
    def update(self) -> None:
        pass

    def __profile_base(self) -> dict:
        return {
            "name": "str",
            "accuracy_average": 0,
            "runs": 0,
            "average_difficulty": 0.00,
            "encounters": {
                "top": {
                    "words": [
                        {
                            "word": "0",
                            "encountered": 0
                        },
                        {
                            "word": "0",
                            "encountered": 0
                        },
                        {
                            "word": "0",
                            "encountered": 0
                        }
                    ],
                    "letters": [
                        {
                            "letter": "0",
                            "encountered": 0
                        }
                    ]
                }
            }
        }


class Word:
    def __init__(self, word: str) -> None:
        self.word: str = word
        self.diff: int = len(word)

        self.letters: list[str] = self.__generate_letters()

    if DEBUG:
        def __log(self) -> None:
            print(self.word)

    def __generate_letters(self) -> list[str]:
        letters: list[str] = []
        for l in self.word:
            letters.append(l)

        return letters

    def value(self) -> str:
        return self.word


class WordList:
    def __init__(self, max_word_length: int, word_count: int) -> None:
        self.max_word_length: int = max_word_length
        self.word_count: int = word_count
        self.words: list[Word] = self.__generate_word_list()
    
    def __load_words(self) -> dict[str, int]:
        with open(pathToWords, 'r') as j:
            return load(j)

    def __generate_word_list(self) -> list[Word]:
        wordList: list[Word] = []
        words: list = list(self.__load_words().keys())

        while len(wordList) < self.word_count:
            word = choice(words)

            if len(word) <= self.max_word_length:
                wordList.append(Word(word))

        return wordList


class App:
    def __init__(self) -> None:
        self.max_word_length: int = 12
        self.word_count: int = 10

        self.word_list: WordList = WordList(self.max_word_length, self.word_count)
        self.profile: Profile = self.__get_profile()

        self._speed: float = 0
        self._input_results: list[Word] = []
        self._results: Text = Text()
        
    def __set_max_word_length(self, max_word_length: int) -> None:
        self.max_word_length = max_word_length

    def __set_word_count(self, word_count: int) -> None:
        self.word_count = word_count

    def __get_profile(self) -> Profile:
        return Profile()

    def __get_word_list(self) -> WordList:
        return WordList(self.max_word_length, self.word_count)

    def __game_splash(self) -> None:
        text: Text = Text('Welcome to TYPY', justify='center')
        style: Style = Style(color='red', bold=True)

        text.stylize(style)
        
        panel: Panel = Panel(
            Padding(text, 1),
            title='TYPY',
            subtitle='https://github.com/Downmoto/typy',
            box=box.ROUNDED,
            style="cyan"
        )
        
        print(panel)

    def __generate_word_panel(self) -> None:
        words: list[str] = [n.value() for n in self.word_list.words]
        words_converted: Text = Text(' '.join(words), justify='center')
        style: Style = Style(color='white')
        
        words_converted.stylize(style)
        
        print(
            Panel(
                words_converted,
                box=box.ROUNDED,
                style='cyan'
            )
        )
        
    def __generate_results_panel(self) -> None:
        print(
            Panel(
                self._results,
                box=box.ROUNDED,
            )
        )

    def __get_input(self) -> None:
        start: float = time()
        results: Union[str, int] = Prompt.ask(
            Text(f"{self.profile.profile['name']} >>", style='green bold'))
        end: float = time()
        
        self._speed = round((end - start), 2)
        
        for word in results.split(' '):
            self._input_results.append(Word(word))

    def __check_input(self) -> None:  
        words: Text = Text(justify='center')

        for i in range(len(self._input_results)):
            input_word: Word = self._input_results[i]
            input_letters: list[str] = input_word.letters

            word_list_word: Word = self.word_list.words[i]
            word_list_letters: list[str] = word_list_word.letters
            
            size: int = max(len(input_word.word), len(word_list_word.word))
            result: Text = Text()

            for j in range(size):
                try:
                    if input_letters[j] == word_list_letters[j]:
                        style: str = 'green bold'
                    else:
                        style: str = 'magenta bold'

                    result.append(input_letters[j], style=style)
                except:                    
                    try:
                        result.append(word_list_letters[j])
                    except:
                        result.append(input_letters[j])

            words.append(result)
            
            if i != len(self._input_results):
                words.append(' ')
            
        self._results = words
                    
    def start(self) -> None:
        self.__game_splash()

        if DEBUG:
            self.__set_max_word_length(int(Prompt.ask('Maximum word length >>')))
            self.__set_word_count(int(Prompt.ask('Word count >>')))
            
        self.word_list = self.__get_word_list()

        self.__generate_word_panel()
        self.__get_input()
        self.__check_input()
        
        self.__generate_results_panel()

        print(self._speed)


def main():
    app: App= App()
    
    app.start()

def debug():
    app: App = App()
    app.start()

if __name__ == '__main__':
    if DEBUG:
        debug()
    else:
        main()
