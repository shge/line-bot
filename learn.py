import markov
import logging

logger = logging.getLogger(__name__)
fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)


"""
1. Load text -> Parse text using MeCab
"""
parsed_text = markov.parse_text('chumon.txt', is_line_messages=False)
logger.info('Parsed text.')

"""
2. Build model
"""
text_model = markov.build_model(parsed_text, format=False, state_size=2)
logger.info('Built text model.')

json = text_model.to_json()
open('chumon.json', 'w').write(json)

# Load from JSON
# json = open('input.json').read()
# text_model = markovify.Text.from_json(json)


"""
3. Make sentences
"""
try:
    for _ in range(10):
        sentence = markov.make_sentences(text_model, start='', max=80, min=20)
        logger.info(sentence)
except KeyError:
    logger.error('KeyError: No sentence starts with "start".')
    logger.info('If you set format=True, please change "start" to another word.')
    logger.info('If you set format=False, you cannot specify "start".')
