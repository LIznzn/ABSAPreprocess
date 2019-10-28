def punc_seperator(text):

    def processing(token):
        punctuation = ",.?!"
        idx = 0
        for i in range(1, len(token)+1):
            if len(token) > 1 and token[-i] in punctuation:
                idx = i
            else:
                break
        if idx == 0:
            return [token]
        else:
            return [token[:-idx], token[-idx:]]

    text_chunks = text.split() # [w1, w2, w3...]
    text_processed_chunks = []

    for token in text_chunks:
        text_processed_chunks.extend(processing(token))

    return text_processed_chunks