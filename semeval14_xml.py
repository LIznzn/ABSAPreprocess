import xml.etree.ElementTree as ET
from utils import punc_seperator
import codecs
import csv


def semeval14_parser(file_path, term_type="aspect", rm_conflict_senti=True):

    if term_type == "join":
        if rm_conflict_senti:
            senti_tag_dict = {"positive": "POS", "negative": "NEG", "neutral": "NEU"}
        else:
            senti_tag_dict = {"positive": "POS", "negative": "NEG", "neutral": "NEU", "conflict": "CON"}

    datas = []

    root = ET.parse(file_path).getroot()

    for sent in root.iter("sentence"):
        opins = []
        for opin in sent.iter("aspectTerm"):
            from_idx = int(opin.attrib["from"])
            to_idx = int(opin.attrib["to"])
            term = opin.attrib["term"]
            if term_type == "join":
                polarity = opin.attrib["polarity"]
            if from_idx != to_idx and term != "NULL":
                if term_type == "join":
                    opins.append((term, from_idx, to_idx, polarity))
                else:
                    opins.append((term, from_idx, to_idx))

        opins = sorted(opins, key=lambda x: x[1])

        text = sent.find("text").text
        text_chunks = []
        label_chunks = []
        prev_i = 0
        for opin_i in opins:

            if term_type == "join":
                opin_i_term, opin_i_from, opin_i_to, opin_i_pol = opin_i
                # remove conflict opinions
                if opin_i_pol == "conflict" and rm_conflict_senti:
                    continue
            else:
                opin_i_term, opin_i_from, opin_i_to = opin_i

            # aspect term left
            tmp_text = text[prev_i:opin_i_from].strip()
            tmp_text = punc_seperator(tmp_text) # [w1, w2, w3, ...]
            tmp_label = ["O"] * len(tmp_text) # [O, O, O, ...]
            text_chunks.extend(tmp_text)
            label_chunks.extend(tmp_label)

            # aspect
            tmp_term = text[opin_i_from:opin_i_to]
            assert tmp_term.lower() == opin_i_term.lower()
            tmp_term = tmp_term.split()
            term_length = len(tmp_term)
            if term_length == 1:
                if term_type == "join":
                    tmp_label = ["B-" + senti_tag_dict[opin_i_pol]]
                else:
                    tmp_label = ["B"]
            else:
                if term_type == "join":
                    tmp_label = ["B-" + senti_tag_dict[opin_i_pol]] + ["I-" + senti_tag_dict[opin_i_pol]]*(term_length-1)
                else:
                    tmp_label = ["B"] + ["I"]*(term_length-1)
            text_chunks.extend(tmp_term) # [w1, w2]
            label_chunks.extend(tmp_label) # [T-POS, T-POS]

            prev_i = opin_i_to

        # rest of the sentences
        tmp_text = text[prev_i:].strip()
        tmp_text = punc_seperator(tmp_text) # [w1, w2, w3, ...]
        tmp_label = ["O"] * len(tmp_text)
        text_chunks.extend(tmp_text)
        label_chunks.extend(tmp_label)

        assert len(text_chunks) == len(label_chunks)
        text_out = " ".join(text_chunks)
        label_out = " ".join(label_chunks)

        datas.append([text_out, label_out])

    return datas

if __name__ == "__main__":

    file_map = {
        "restaurant": {
            "train": ("datasets/SemEval2014/train/Restaurants_Train_v2.xml", "aspect"), # join/aspect
            "test": ("datasets/SemEval2014/test/Restaurants_Test_Data_phaseB.xml", "aspect")
        },
        "laptop": {
            "train": ("datasets/SemEval2014/train/Laptop_Train_v2.xml", "aspect"), # join/aspect
            "test": ("datasets/SemEval2014/test/Laptops_Test_Data_phaseB.xml", "aspect")
        }
    }

    for dataset, dataset_value in file_map.items():
        for train_test, file_param_value in dataset_value.items():
            datas = semeval14_parser(file_path=file_param_value[0], term_type=file_param_value[1])
            out_path = "datasets/SemEval2014/mydata/{}_{}_{}_{}.csv".format(dataset, train_test, file_param_value[1], len(datas))
            with codecs.open(out_path, "w", "utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(datas)


