import sys
import os
import re
out = open("nbmodel.txt", "w")
vocab = []

positive = "/positive_polarity/"
negative = "/negative_polarity/"
positive_truth = "/positive_polarity/truthful_from_TripAdvisor"
positive_deception = "/positive_polarity/deceptive_from_MTurk"
negative_truth = "/negative_polarity/truthful_from_Web"
negative_deception = "/negative_polarity/deceptive_from_MTurk"
stop_words = stopList = ['a','about','above','after','again','against','all','am','an','and','any','are','arent','as','at','be','because','been','before','being','below','between','both','but','by','cant','cannot','could','couldnt','did','didnt','do','does','doesnt','doing','dont','down','during','each','few','for','from','further','had','hadnt','has','hasnt','have','havent','having','he','hed','hell','hes','her','here','heres','hers','herself','him','himself','his','how','hows','i','id','ill','im','ive','if','in','into','is','isnt','it','its','its','itself','lets','me','more','most','mustnt','my','myself','no','nor','not','of','off','on','once','only','or','other','ought','our','ours','ourselves','out','over','own','same','shant','she','shed','shell','shes','should','shouldnt','so','some','such','than','that','thats','the','their','theirs','them','themselves','then','there','theres','these','they','theyd','theyll','theyre','theyve','this','those','through','to','too','under','until','up','very','was','wasnt','we','wed','well','were','weve','were','werent','what','whats','when','whens','where','wheres','which','while','who','whos','whom','why','whys','with','wont','would','wouldnt','you','youd','youll','youre','youve','your','yours','yourself','yourselves']


def get_files(root_dir):
    filesL = []
    for rot, dirs, files in os.walk(root_dir):
        for fN in files:
            if fN.endswith(".txt"):
                filesL.append(os.path.join(rot, fN))
    return filesL


def get_dict(fl, d):
    for file_path in fl:
        words = open(file_path, "r").read()
        words = re.sub('[^a-zA-Z]', ' ', words).lower()
        for word in words.split():
            if word not in stop_words:
                if word not in vocab:
                    vocab.append(word)
                if word in d:
                    d[word] += 1
                else:
                    d[word] = 1
    return d


def normalize(d):
    for word in vocab:
        if word not in d:
            d[word] = 0
    return d


def build_model(d, t):
    out.write(t + " " + str(len(d.keys())) + " " + str(sum(d.values())) + "\n")
    for key, elem in d.items():
        out.write(key + " " + str(elem) + "\n")


def main():
    root = sys.argv[1]
    pos = dict()
    neg = dict()
    truth = dict()
    decp = dict()
    files = get_files(root+positive)
    pos = get_dict(files, pos)
    files = get_files(root+negative)
    neg = get_dict(files, neg)
    pos = normalize(pos)
    neg = normalize(neg)
    del vocab[:]
    files = get_files(root+positive_truth)
    truth = get_dict(files, truth)
    files = get_files(root+positive_deception)
    decp = get_dict(files, decp)
    files = get_files(root+negative_truth)
    truth = get_dict(files, truth)
    files = get_files(root+negative_deception)
    decp = get_dict(files, decp)
    truth = normalize(truth)
    decp = normalize(decp)
    build_model(pos, "POSITIVE")
    build_model(neg, "NEGATIVE")
    build_model(truth, "TRUTHFUL")
    build_model(decp, "DECEPTIVE")
main()
