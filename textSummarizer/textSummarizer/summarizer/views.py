from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation



# from django.shortcuts import render
from json import dumps

# Create your views here.
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def homepageview(request):
    return render(request,'index.html')

def ajax_test(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        text_Data = request.GET.get('text_Data')
        # import en_core_web_sm

        # nlp = en_core_web_sm.load()
        # from heapq import nlargest
        # select_length = int(len(sentence_tokens)*.30)
        # summary = nlargest(select_length,sentence_scores, key = sentence_scores.get)
        # final_summary = [word.text for word in summary]
        # summary = ' '.join(final_summary)

        
        nlp = spacy.load("en_core_web_lg")
        doc = nlp(text_Data)
        type(doc)
        tokens = [token.text for token in doc]
        from string import punctuation
        punctuation += '\n'
        tokens = [token for token in tokens if token not in punctuation]
        word_frequencies = {}
        for word in doc:
            if word.text.lower() not in punctuation:
                if word.text.lower() not in list(STOP_WORDS):
                    if word.text not in word_frequencies.keys():
                        word_frequencies[word.text] = 1
                    else:
                        word_frequencies[word.text] += 1
        # message = "This is ajax"
        # print(text_Data)
        max_frequency = max(word_frequencies.values())
        max_keys = []
        for key,value in word_frequencies.items():
            if value == max_frequency:
                max_keys.append(key)

        for word in word_frequencies.keys():
            word_frequencies[word] = word_frequencies[word]/max_frequency
        
        sentence_tokens = [sent for sent in doc.sents]
        sentence_scores = {}
        for sent in sentence_tokens:
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]
        from heapq import nlargest
        select_length = int(len(sentence_tokens)*.30)
        summary = nlargest(select_length,sentence_scores, key = sentence_scores.get)
        final_summary = [word.text for word in summary]
        summary = ' '.join(final_summary)
        # print(summary)
        return JsonResponse({'cols': summary})

    return JsonResponse({'cols': text_Data})



def ajax_test2(request):

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        text_Data = request.GET.get('text_Data')
        import torch
        from transformers import T5Tokenizer, T5ForConditionalGeneration,T5Config
        model  = T5ForConditionalGeneration.from_pretrained('t5-small')
        tokernizer = T5Tokenizer.from_pretrained('t5-small')
        device = torch.device('cpu')
        text = text_Data
        
        # preprocessing
        preprocessed_text = text.strip().replace('\n','')
        t5_input_text = "summary: " + preprocessed_text
        tokenized_text = tokernizer.encode(t5_input_text,return_tensors ='pt',max_length=512).to(device)

        # summarize

        summary_ids = model.generate(tokenized_text,min_length=30,max_length=30)
        summary = tokernizer.decode(summary_ids[0],skip_special_tokens=True)

        return JsonResponse({'cols':summary})


    return JsonResponse({'cols':text_Data})