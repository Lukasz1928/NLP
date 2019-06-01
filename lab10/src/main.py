import sentencepiece as sp
from fastai.text import *


def get_sentencepiece_processor(paths):
    spp = sp.SentencePieceProcessor()
    spp.Load(paths['sp_model'])

    spp.SetEncodeExtraOptions("bos:eos")
    spp.SetDecodeExtraOptions("bos:eos")
    return spp


def get_language_model(bptt, max_seq, n_tok, emb_sz, n_hid, n_layers, pad_token, paths, bidir=False, tie_weights=True, qrnn=False):
    mb_rnn = MultiBatchRNN(bptt, max_seq, n_tok, emb_sz, n_hid, n_layers, pad_token=pad_token, bidir=bidir, qrnn=qrnn)
    s_rnn = SequentialRNN(mb_rnn, LinearDecoder(n_tok, emb_sz, 0, tie_encoder=mb_rnn.encoder if tie_weights else None))
    s_rnn = to_gpu(s_rnn)
    load_model(s_rnn[0], paths['fastai_model'])
    s_rnn.reset()
    s_rnn.eval()
    return s_rnn


class SentenceDataset(Dataset):
    def __init__(self, x):
        self.x = x

    def __getitem__(self, idx):
        return self.x[idx][:-1], self.x[idx][1:]


def next_token(sentence, model, spp):
    ids = [np.array(spp.encode_as_ids(sentence))]
    dataset = SentenceDataset(ids)
    sampler = SortSampler(ids, key=lambda x: len(ids[x]))
    dl = DataLoader(dataset,
                    batch_size=100,
                    transpose=True,
                    pad_idx=1,
                    sampler=sampler,
                    pre_pad=False)

    t = None
    with no_grad_context():
        for (x, y) in dl:
            t, _, _ = model(x)

    best_word_id = int(torch.argmax(t[-1]))
    best_word = spp.decode_ids([best_word_id])

    while best_word in [",", ".", ";", " ", ""]:
        t[-1][best_word_id] = -1
        best_word_id = int(torch.argmax(t[-1]))
        best_word = spp.decode_ids([best_word_id])
    return best_word


def predict_next(sentence, model, spp, words_to_predict):
    r = "[{}]".format(sentence)
    current = sentence
    for _ in range(words_to_predict):
        predicted_word = next_token(current, model, spp)
        r += " " + predicted_word
        current += " " + predicted_word
    return r


def main():
    model_files_paths = {'fastai_model': '../data/work/up_low50k/models/fwd_v50k_finetune_lm_enc.h5',
                         'sp_model': '../data/work/up_low50k/tmp/sp-50k.model',
                         'sp_vocab': '../data/work/up_low50k/tmp/sp-50k.vocab'}

    spp = get_sentencepiece_processor(model_files_paths)
    lm = get_language_model(5, 1000000, len(spp), 400, 1150, 4, 1, model_files_paths)
    
    to_predict = ['Warszawa to największe',
                  'Te zabawki należą do',
                  'Policjant przygląda się',
                  'Na środku skrzyżowania widać',
                  'Właściciel samochodu widział złodzieja z',
                  'Prezydent z premierem rozmawiali wczoraj o',
                  'Witaj drogi']
    to_predict2 = ['Gdybym wiedział wtedy dokładnie to co wiem teraz, to bym się nie',
                   'Gdybym wiedziała wtedy dokładnie to co wiem teraz, to bym się nie']
    to_predict_long = ('Polscy naukowcy odkryli w Tatrach nowy gatunek istoty żywej. '
                      'Zwięrzę to przypomina małpę, lecz porusza się na dwóch nogach i potrafi posługiwać się narzędziami. ' 
                      'Przy dłuższej obserwacji okazało się, że potrafi również posługiwać się językiem polskim, '
                      'a konkretnie gwarą podhalańską. Zwierzę to zostało nazwane')
    with open('../results/results.txt', 'w+', encoding='utf-8') as f:
        for tp in to_predict:
            pred = predict_next(tp, lm, spp, 20)
            f.write('{}\n'.format(pred))
        f.write('\n')
        for tp in to_predict2:
            pred = predict_next(tp, lm, spp, 20)
            f.write('{}\n'.format(pred))
        f.write('\n')
        pred = predict_next(to_predict_long, lm, spp, 50)
        f.write('{}\n'.format(pred))
    

if __name__ == '__main__':
    main()

