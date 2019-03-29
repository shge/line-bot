import logging
import markovify
import MeCab

logger = logging.getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)


# Load file
# text_file = open("input.txt", "r")
# text = text_file.read()
# logger.info('File loaded')


# Parse text using MeCab
parsed_text = ''
for line in open('input.txt', 'r'):
    parsed_text += MeCab.Tagger('-Owakati').parse(line)
parsed_text = parsed_text.rstrip('\n')
# TODO:。で改行
logger.info('Text parsed')


# Build model
text_model = markovify.NewlineText(parsed_text, state_size=2)
logger.info('Text model built')


# Output (max, min)
# for _ in range(10):
sentence = text_model.make_short_sentence(100, 30, tries=100).replace(' ', '')
logger.info(sentence)
