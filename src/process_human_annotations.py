import itertools

import argparse
import ast
import json
import newlinejson
import os

RELATION_DICT_REL_IDX = {
    'who': 1,
    'what': 2,
    'what_happened': 3,
    'what_happens': 4,
    'what_will_happen': 5,
    'where': 6,
    'when': 7,
    'why': 8,
}

RELATION_DICT_IDX_REL = {
    1: 'WHO',
    2: 'WHAT',
    3: 'WHAT_HAPPENED',
    4: 'WHAT_HAPPENS',
    5: 'WHAT_WILL_HAPPEN',
    6: 'WHERE',
    7: 'WHEN',
    8: 'WHY',
}


def find_tok_idx(sublst, lst, sent_idx, sent_len_dict):
    """ Based on: https://stackoverflow.com/questions/17870544/find-starting-and-ending-indices-of-sublist-in-list"""
    len_sublst = len(sublst)

    for ind in (i for i, e in enumerate(lst) if e == sublst[0]):
        if lst[ind:ind + len_sublst] == sublst:
            start = ind
            end = ind + len_sublst - 1

            len_before = 0
            for s_i in range(sent_idx):
                len_before += sent_len_dict[s_i]

            return start + len_before, end + len_before


def mturk_labels_to_dygiepp(label_file, out_file):
    with open(label_file, 'r') as lf:
        label_dict = json.load(lf)

    with newlinejson.open(out_file, 'w') as out_f:

        for doc_id, dicts in label_dict.items():

            tok_abstract = ast.literal_eval(dicts['tok_abstract'])

            for ann, ann_dict in dicts['annotations'].items():

                abs_dict = {}
                abs_dict['doc_key'] = 'hl_{}_{}'.format(doc_id, ann)
                abs_dict['dataset'] = dicts['dataset']
                abs_dict['sentences'] = [list(itertools.chain.from_iterable(tok_abstract))]  # tok_abstract
                abs_dict['relations'] = [[]]  # everything as a single sentence

                sent_len_dict = {}
                for i, s in enumerate(tok_abstract):
                    sent_len_dict[i] = len(s)

                sent_accum_len_dict = {}
                current_len = 0
                for i, s in enumerate(tok_abstract):
                    sent_accum_len_dict[i] = current_len
                    current_len += len(s)  # added after, so that we can use it below immediately

                triples_ids = ann_dict['triples_ids']
                sents_ids = ann_dict['sent_ids']

                for triple_ids, sent_ids in zip(triples_ids, sents_ids):
                    sent_idx_a = sent_ids[0]
                    len_so_far_a = sent_accum_len_dict[sent_idx_a]
                    sent_idx_b = sent_ids[1]
                    len_so_far_b = sent_accum_len_dict[sent_idx_b]

                    start_a = triple_ids[0]
                    end_a = triple_ids[1]
                    relation_id = triple_ids[2]
                    start_b = triple_ids[3]
                    end_b = triple_ids[4]

                    relation_capitalized = RELATION_DICT_IDX_REL[relation_id]

                    # Print statements to double check whether your triples make sense
                    print(' '.join(tok_abstract[sent_idx_a][start_a:end_a + 1]))
                    print(relation_capitalized)
                    print(' '.join(tok_abstract[sent_idx_b][start_b:end_b + 1]))

                    abs_dict['relations'][0].append(
                        [start_a + len_so_far_a, end_a + len_so_far_a, start_b + len_so_far_b, end_b + len_so_far_b,
                         relation_capitalized])

                out_f.write(abs_dict)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process human annotations')
    parser.add_argument('--label_file', description='label file including the tokenized abstracts', required=True)
    parser.add_argument('--out_dir', description='output directory for processed data', required=True)
    parser.add_argument('--out_file', description='output file for processed data', required=True)

    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    mturk_labels_to_dygiepp(args.label_file, '{}/{}'.format(args.out_dir, args.out_file))
