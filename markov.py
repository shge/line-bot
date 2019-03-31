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

def parse_line(t):
    t = t.replace('[Sticker]', '').replace('[Photo]', '').replace('[Voice message]', '').replace('[File]', '')
    t = re.sub(r'\[LINE\] Chat history .+$', '', t, flags=re.MULTILINE)  # 1st line
    t = re.sub(r'^Saved on: .+$', '', t, flags=re.MULTILINE)  # 2nd line
    t = re.sub(r'^..../../.. ...$', '', t, flags=re.MULTILINE)  # Date
    t = re.sub(r'^..:..\t.+\t', '', t, flags=re.MULTILINE)  # Date and time
    t = re.sub(r'^http.+', '', t, flags=re.MULTILINE)  # URL
    t = re.sub(r'^..:..\t.+\.$', '', t, flags=re.MULTILINE)  # Messages
    t = re.sub(r'^☎ .+', '', t, flags=re.MULTILINE)  # ☎
    t = re.sub(r'\n+', r'\n', t).strip('\n')  # Empty lines
    return t

def format_text(t):
    t = t.replace('　', ' ')  # Full width spaces
    # t = re.sub(r'([。．！？…]+)', r'\1\n', t)  # \n after ！？
    t = re.sub(r'(.+。) (.+。)', r'\1 \2\n', t)
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'([。．！？…])\n」', r'\1」 \n', t)  # \n before 」
    t = re.sub(r'\n +', '\n', t)  # Spaces
    t = re.sub(r'\n+', r'\n', t).rstrip('\n')  # Empty lines
    t = re.sub(r'\n +', '\n', t)  # Spaces
    return t

def parse_text(filepath, is_line_messages=False):
    file = open(filepath, 'r').read()

    if is_line_messages is True:
        file = parse_line(file)
        logger.info('Parsed text with LINE parser.')

    parsed_text = ''
    for line in file.split("\n"):    # To retain \n for e.g. LINE messages
        parsed_text = parsed_text + MeCab.Tagger('-Owakati').parse(line)
    return parsed_text

def build_model(text, format=True, state_size=2):
    """
    format=True: Fast. Recommended for LINE.
    format=False: Slow. Funnier(?)
    """
    if format is True:
        logger.info('Format: True')
        return markovify.NewlineText(format_text(text), state_size)
    else:
        logger.info('Format: False')
        # text = text.replace('\n', ' ')
        disable_test_sentence_input()
        text = markovify.Text(text, state_size)
        enable_test_sentence_input()
        return text

def make_sentences(text, start=None, max=300, min=1, tries=100):
    if start is (None or ''):   # If start is not specified
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
