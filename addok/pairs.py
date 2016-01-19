from addok import config, hooks
from addok.helpers.index import token_key, preprocess_housenumber


def pair_key(s):
    return 'p|{}'.format(s)


def pairs_indexer(pipe, key, doc, tokens, **kwargs):
    els = set(tokens.keys())  # Unique values.
    for el in els:
        values = set([])
        for el2 in els:
            if el != el2:
                values.add(el2)
        if values:
            pipe.sadd(pair_key(el), *values)


def pairs_deindexer(db, key, doc, tokens, **kwargs):
    els = list(set(tokens))  # Unique values.
    loop = 0
    for el in els:
        for el2 in els[loop:]:
            if el != el2:
                key = '|'.join(['didx', el, el2])
                # Do we have other documents that share el and el2?
                commons = db.zinterstore(key, [token_key(el), token_key(el2)])
                db.delete(key)
                if not commons:
                    db.srem(pair_key(el), el2)
                    db.srem(pair_key(el2), el)
        loop += 1


def housenumbers_pairs_indexer(pipe, key, doc, tokens, **kwargs):
    housenumbers = doc.get(config.HOUSENUMBERS_FIELD)
    if not housenumbers:
        return
    for number in housenumbers.keys():
        for hn in preprocess_housenumber(number.replace(' ', '')):
            # Pair every document term to each housenumber, but do not pair
            # housenumbers together.
            pipe.sadd(pair_key(hn), *tokens.keys())


def housenumbers_pairs_deindexer(db, key, doc, tokens, **kwargs):
    for field, value in doc.items():
        field = field.decode()
        if not field.startswith('h|'):
            continue
        number, lat, lon, *extra = value.decode().split('|')
        hn = field[2:]
        for token in tokens:
            k = '|'.join(['didx', hn, token])
            commons = db.zinterstore(k, [token_key(hn), token_key(token)])
            db.delete(k)
            if not commons:
                db.srem(pair_key(hn), token)
                db.srem(pair_key(token), hn)


@hooks.register
def addok_configure(config):
    target = 'addok.helpers.index.document_indexer'
    if target in config.INDEXERS:
        idx = config.INDEXERS.index(target)
        config.INDEXERS.insert(idx, pairs_indexer)
    target = 'addok.helpers.index.housenumbers_indexer'
    if target in config.INDEXERS:
        idx = config.INDEXERS.index(target)
        config.INDEXERS.insert(idx, housenumbers_pairs_indexer)
    target = 'addok.helpers.index.document_deindexer'
    if target in config.DEINDEXERS:
        idx = config.DEINDEXERS.index(target)
        config.DEINDEXERS.insert(idx, pairs_deindexer)
    target = 'addok.helpers.index.housenumbers_deindexer'
    if target in config.DEINDEXERS:
        idx = config.DEINDEXERS.index(target)
        config.DEINDEXERS.insert(idx, housenumbers_pairs_deindexer)
