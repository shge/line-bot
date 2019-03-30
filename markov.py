import logging
import markovify
import MeCab
import re

logger = logging.getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)


# Toggle test_sentence_input
test_sentence_input = markovify.Text.test_sentence_input  # Stash
def disable_test_sentence_input():
    def do_nothing(self, sentence):
        return True
    markovify.Text.test_sentence_input = do_nothing
def enable_test_sentence_input():
    markovify.Text.test_sentence_input = test_sentence_input


def format_book(t):
    t = t.replace('　', ' ')  # Full width spaces
    t = re.sub(r'([。．！？…]+)', r'\1\n', t)  # \n after ！？
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'([。．！？…])\n」', r'\1」 \n', t)  # \n before 」
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'\n+', r'\n', t).rstrip('\n')  # Empty lines
    t = re.sub(r'\n +', '\n', t)  # Spaces
    # t = re.sub(r'。\n「', '。「\n「', t)  # Spaces
    return t


def make_sentences(text, start=None, max=300, min=1, tries=100):
    if start is None:   # If start is specified
        for _ in range(tries):
            sentence = str(text.make_sentence()).replace(' ', '')
            if sentence and len(sentence) <= max and len(sentence) >= min:
                return sentence
    else:  # If start is specified
        for _ in range(tries):
            sentence = str(text.make_sentence_with_start(beginning=start)).replace(' ', '')
            if sentence and len(sentence) <= max and len(sentence) >= min:
                return sentence


# json = open("model.json", "r").read()
# text_model = markovify.Text.from_json(json)


"""
1. Load text -> Parse text using MeCab
"""
parsed_text = ''
for line in open('input.txt', 'r'):    # To retain \n for e.g. LINE messages
    parsed_text = parsed_text + '' + MeCab.Tagger('-Owakati').parse(line)


"""
2. Format text
"""
formatted_text = format_book(parsed_text)
logger.info('Text formatted')


"""
3. Build model
"""
text_model = markovify.NewlineText(formatted_text, state_size=2)
logger.info('Text model built')

# parsed_text = parsed_text.replace('\n', '')
# disable_test_sentence_input()
# text_model = markovify.Text(parsed_text, state_size=2)
# enable_test_sentence_input()

"""
4. Make sentences
"""
for _ in range(5):
    sentence = make_sentences(text_model, start='メロス', max=300, min=30)
    logger.info(sentence)
