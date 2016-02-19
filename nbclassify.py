import sys
import os
import re
import math
positive = dict()
negative = dict()
truthful = dict()
deceptive = dict()
stop_words = stopList = ['a','about','above','after','again','against','all','am','an','and','any','are','arent','as','at','be','because','been','before','being','below','between','both','but','by','cant','cannot','could','couldnt','did','didnt','do','does','doesnt','doing','dont','down','during','each','few','for','from','further','had','hadnt','has','hasnt','have','havent','having','he','hed','hell','hes','her','here','heres','hers','herself','him','himself','his','how','hows','i','id','ill','im','ive','if','in','into','is','isnt','it','its','its','itself','lets','me','more','most','mustnt','my','myself','no','nor','not','of','off','on','once','only','or','other','ought','our','ours','ourselves','out','over','own','same','shant','she','shed','shell','shes','should','shouldnt','so','some','such','than','that','thats','the','their','theirs','them','themselves','then','there','theres','these','they','theyd','theyll','theyre','theyve','this','those','through','to','too','under','until','up','very','was','wasnt','we','wed','well','were','weve','were','werent','what','whats','when','whens','where','wheres','which','while','who','whos','whom','why','whys','with','wont','would','wouldnt','you','youd','youll','youre','youve','your','yours','yourself','yourselves']
out = open("nboutput.txt","w")


def get_files(root_dir):
    filesL = []
    for rot, dirs, files in os.walk(root_dir):
        for fN in files:
            if fN.endswith(".txt"):
                filesL.append(os.path.join(rot, fN))
    return filesL


def read_model():
    f = open("nbmodel.txt", "r")
    p_len, p_count = read_positives(f)
    n_len, n_count = read_negatives(f)
    t_len, t_count = read_truthful(f)
    d_len, f_count = read_deceptive(f)
    files = get_files(sys.argv[1])
    for fl in files:
        words = open(fl, "r").read()
        words = re.sub('[^a-zA-Z]', ' ', words).lower()
        pos_prio = math.log(0.5)
        neg_prio = math.log(0.5)
        truth_prio = math.log(0.5)
        decep_prio = math.log(0.5)
        for word in words.split():
            if word not in stop_words:
                if word in positive:
                    pos_prio += math.log((float(positive[word]) + 1) / (p_len + p_count))
                if word in negative:
                    neg_prio += math.log((float(negative[word]) + 1) / (n_len + n_count))
                if word in truthful:
                    truth_prio += math.log((float(truthful[word]) + 1) / (t_len + t_count))
                if word in deceptive:
                    decep_prio += math.log((float(deceptive[word]) + 1) / (d_len + f_count))
        if truth_prio > decep_prio:
            out.write("truthful ")
        else:
            out.write("deceptive ")
        if pos_prio > neg_prio:
            out.write("positive "+fl+"\n")
        else:
            out.write("negative "+fl+"\n")


def read_positives(f):
    header = f.readline().split()
    if "POSITIVE" in header:
        tp_count = int(header[1])
        tp_sum = float(header[2])
        for i in range(tp_count):
            word = f.readline().split()
            positive[word[0]] = float(word[1])
    return tp_count, tp_sum


def read_negatives(f):
    header = f.readline().split()
    if "NEGATIVE" in header:
        fp_count = int(header[1])
        fp_sum = float(header[2])
        for i in range(fp_count):
            word = f.readline().split()
            negative[word[0]] = float(word[1])
    return fp_count, fp_sum


def read_truthful(f):
    header = f.readline().split()
    if "TRUTHFUL" in header:
        tn_count = int(header[1])
        tn_sum = float(header[2])
        for i in range(tn_count):
            word = f.readline().split()
            truthful[word[0]] = float(word[1])
    return tn_count, tn_sum


def read_deceptive(f):
    header = f.readline().split()
    if "DECEPTIVE" in header:
        fn_count = int(header[1])
        fn_sum = float(header[2])
        for i in range(fn_count):
            word = f.readline().split()
            deceptive[word[0]] = float(word[1])
    return fn_count, fn_sum

read_model()

