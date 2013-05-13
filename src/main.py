#!/usr/bin/env python
# encoding: utf-8

'''Clustering Tool.

Usage:
    cluster <directory> [--stop-words=<sw_file>] [--verbose|-v] [--quiet|-q] [--show-no-gui] [--language=<lang>]
    cluster -h|--help
    cluster -V| --version

Options:
    -h --help               Show this message. [default: No]
    -v --verbose            Print debugging output. [default: No]
    -q --quiet              Keep quiet, do not print profiling output. [default: No]
    -V --version            Show version info and authors.[default: No]
    --stop-words=<sw_file>  Load stopwords from this file [default: stopwords.list].
    --language=<lang>       Set the Language used by Porter Stemmer [default: german].
    --show-no-gui           Do not build up GUI after calculations. [default: No]
'''

__version__ = '0.01'
__authors__ = ['ccwelich', 'cpahl', 'cpiechula']


# System libs
import sys
import logging

# Option parsing
from docopt import docopt

# Own modules
import calculations as calc
import vocabular as voc
from timing import timing

from maketree2 import Distance, maketree, build_cluster_tree
from cluster2 import * 
from gui import show_treevis


def get_stopwords(sw_path):
    try:
        with open(sw_path, 'r') as f:
            return set([voc.sanitize_word(word) for word in f.read().split()])
    except FileNotFoundError:
        logging.warning('No file called <%s>, use --stop-words' % sw_path)
        sys.exit(-1)


def main(options):
    voc.set_stemmer(options['--language'])

    # Read vocabulary and documents
    with timing('Fetching stopwords'):
        stopwords = get_stopwords(options['--stop-words'])
        logging.debug("Stopwords:\n%s" % stopwords)

    with timing('Reading directory contents'):
        docs = voc.read_directory(options['<directory>'], stopwords)

    # Join vocabulary to a whole one
    vocabular = []
    for doc in docs:
        vocabular += doc.vocs

    with timing('%d Documents with %d distinct words' % (len(docs), len(vocabular))):
        pass

    with timing('Deduplicating vocabulary'):
        vocabular = list(set(vocabular))
        logging.debug("Full vocabulary:\n%s" % vocabular)

    with timing('Calculating Termfrequency'):
        termfreq = calc.termfreq(docs, vocabular)
        logging.debug("Termfreq:\n%s" % termfreq)

    with timing('Calculating Bag of Words'):
        bag_of_words = calc.bag_of_words(termfreq)
        logging.debug("Bag of Words:\n%s" % bag_of_words)

    with timing('Calculating Max terms per Document'):
        v_max = calc.max_per_doc(termfreq)
        logging.debug("v_max:\n%s" % v_max)

    with timing('Calculating Normalized Termfrequency'):
        norm_termfreq = calc.normalized_term_freq(termfreq, v_max)
        logging.debug("Normed Termfreq:\n%s" % norm_termfreq)

    with timing('Calculating Inverse Document Frequency'):
        inverse_doc_freq = calc.inverse_doc_freq(len(docs), bag_of_words)
        logging.debug("Inverse Doc Freq:\n%s" % inverse_doc_freq)

    with timing('Calculating Weight Matrix'):
        weight_matrix = calc.weight_matrix(norm_termfreq, inverse_doc_freq)
        logging.debug("Weight Vec:\n%s" % weight_matrix)

    with timing('Calculating Document Vector Length'):
        document_abs = calc.document_abs(weight_matrix)
        logging.debug("Document Abs:\n%s" % document_abs)

    # Build hierachical clusters from the weight_matrix
    cluster_tree = build_cluster_tree(
            docs, weight_matrix, document_abs,
            norm_termfreq, termfreq, vocabular
    )

    # Visualize the tree
    if not options['--show-no-gui']:
        show_treevis(cluster_tree)


if __name__ == '__main__':
    options = docopt(__doc__, version=' by '.join([__version__, ', '.join(__authors__)]))

    logging.basicConfig(format='%(message)s')
    root_logger = logging.getLogger()
    if options['--verbose']:
        root_logger.setLevel(logging.DEBUG)
    elif options['--quiet']:
        root_logger.setLevel(logging.WARNING)
    else:
        root_logger.setLevel(logging.INFO)

    logging.debug(options)
    main(options)
