import nltk
import spacy

nlp = spacy.load('en_core_web_md')


def tokenize_abstract(abstract):
    tok_abstract = []
    full_abstract = ' '.join(abstract)
    sent_abstract = list(nlp(full_abstract).sents)

    for sent_idx, sent in enumerate(sent_abstract):
        parsed_string = sent._.parse_string
        tree = nltk.Tree.fromstring(parsed_string)
        tokens = tree.leaves()

        tok_abstract.append(tokens)

    return tok_abstract


