#!/usr/bin/env python

"""
This a script that takes the result of automatic postediting encoded as a
sequence of <keep>, <delete> and insert operations and applies them on the
original text being post-edited.

The inverse script to this one is 'post_edit_prepare_data.py'.
"""

import numpy as np
from language_utils import GermanPreprocessor, GermanPostprocessor
from learning_utils import log, load_tokenized

def reconstruct(source, edits):
    keep='<keep>'
    delete='<delete>'

    index = 0
    target = []

    for edit in edits:
        if edit == '<keep>':
            if index < len(source):
                target.append(source[index])
            index += 1

        elif edit == '<delete>':
            index += 1

        else:
            target.append(edit)

    # we may have created a shorter sequence of edit ops due to the
    # decoder limitations -> now copy the rest of source
    if index < len(source):
        target.extend(source[index:])

    return target


if __name__ == '__main__':
    #edits = ['<keep>', 'ahoj', '<delete>', 'proc?']
    #source = ['Karle', 'co', 'kdy']
    #print reconstruct(source, edits)

    import argparse

    parser = argparse.ArgumentParser(description="Convert postediting target data to sequence of edits")
    parser.add_argument("--edits", type=argparse.FileType('r'), required=True)
    parser.add_argument("--translated-sentences", type=argparse.FileType('r'), required=True)
    parser.add_argument("--target-german", type=bool, default=False)

    args = parser.parse_args()

    postprocess = lambda x: x
    preprocess = None
    if args.target_german:
        postprocess = GermanPostprocessor()
        preprocesss = GermanPreprocessor()

    trans_sentences = load_tokenized(args.translated_sentences, preprocess=preprocess)
    edit_sequences = load_tokenized(args.edits, preprocess=None)

    for trans, edits in zip(trans_sentences, edit_sequences):
        target = reconstruct(trans, edits)
        print " ".join(postprocess(target))

