import re
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

def simple_summarize(text: str, sentences_count: int = 2) -> str:
    if not text:
        return ""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    valid = [s for s in sentences if len(s.strip()) > 10]
    return " ".join(valid[:sentences_count]) if valid else text[:200] + "..."

def nlp_summarize(text: str, sentences_count: int = 2, lang: str = "russian") -> str:
    try:
        if not text or len(text) < 100:
            return simple_summarize(text, sentences_count)

        parser = PlaintextParser.from_string(text, Tokenizer(lang))
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, sentences_count)
        return " ".join(str(sentence) for sentence in summary)
    except Exception as e:
        return simple_summarize(text, sentences_count)