import logging
import markovify
import MeCab
import re

logger = logging.getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)


def make_short_sentences(text, max=300, min=0, tries=100):
    for _ in range(tries):
        sentence = text.make_sentence().replace(' ', '')
        if sentence and len(sentence) <= max and len(sentence) >= min:
            return sentence

def make_short_sentences_with_start(text, beginning, max=300, min=0, tries=100):
    for _ in range(tries):
        sentence = text.make_sentence_with_start(beginning).replace(' ', '')
        if sentence and len(sentence) <= max and len(sentence) >= min:
            return sentence


# Load file
# text = open("input.txt", "r").read()
# logger.info('File loaded')


# Parse text using MeCab
parsed_text = ''
for line in open('input.txt', 'r'):
    parsed_text += MeCab.Tagger('-Owakati').parse(line)
parsed_text = parsed_text.rstrip('\n')
parsed_text = re.sub('[。．](.)', '。\n\1', parsed_text)
# logger.info('Text parsed')


# Build model
# text_model = markovify.Text(parsed_text, state_size=2)
text_model = markovify.NewlineText(parsed_text, state_size=2)
logger.info('Text model built')


# Output (max, min)
for _ in range(10):
    # sentence = make_short_sentences(text_model, max=100, min=50)
    sentence = make_short_sentences_with_start(text_model, 'メロス', max=30, min=5)
    logger.info(sentence)
