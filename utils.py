from string import punctuation

def punc_seperator(text):

    def processing(token):
        # punctuation = ",.?!-():"
        backward_idx = 0
        forward_idx = -1
        # forward
        for i in range(1, len(token)+1):
            if len(token) > 1 and token[-i] in punctuation:
                backward_idx = i
            else:
                break
        for i in range(len(token)):
            if len(token) > 1 and token[i] in punctuation:
                forward_idx = i+1
            else:
                break
        if (backward_idx == 0 and forward_idx == -1) or backward_idx == forward_idx:
            return [token]
        if backward_idx != 0 and forward_idx != -1:
            return [token[:forward_idx], token[forward_idx:-backward_idx], token[-backward_idx:]]
        if forward_idx != -1:
            return [token[:forward_idx], token[forward_idx:]]
        if backward_idx != 0:
            return [token[:-backward_idx], token[-backward_idx:]]

    text_chunks = text.split() # [w1, w2, w3...]
    text_chunks = [chunk.strip() for chunk in text_chunks if chunk.strip() != ""] # remove space
    text_processed_chunks = []

    for token in text_chunks:
        text_processed_chunks.extend(processing(token))

    return text_processed_chunks


if __name__ == "__main__":

    s = ")."

    print(punc_seperator(s))