from collections import Counter, defaultdict

import uvicorn
from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
from starlette.datastructures import State


class WordListProcessor:
    def __init__(self, file_path: str = "mywordlist.txt"):
        self.word_dict = defaultdict(list)
        self.preprocess_wordlist(file_path)

    def preprocess_wordlist(self, file_path: str):
        with open(file_path, "r") as file:
            for line in file:
                word = line.strip()
                word_signature = frozenset(Counter(word).items())
                self.word_dict[word_signature].append(word)

    def get_permutations(self, word: str):
        word_signature = frozenset(Counter(word).items())
        return self.word_dict.get(word_signature, [])


app = FastAPI()
app.state = State()


def get_word_processor() -> WordListProcessor:
    if not hasattr(app.state, "word_processor"):
        app.state.word_processor = WordListProcessor()
    return app.state.word_processor


@app.get("/permutations")
async def get_permutations(
    word: str = Query(...), processor: WordListProcessor = Depends(get_word_processor)
):
    permutations = processor.get_permutations(word)
    return JSONResponse(content=permutations)


@app.on_event("startup")
async def setup_word_processor():
    app.state.word_processor = WordListProcessor()


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
