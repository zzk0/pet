from transformers import pipeline, AutoModelForMaskedLM, AutoTokenizer
from xunfei import XunfeiApi

# bert mask
model_path = '/home/percent1/models/nlp/text-classification/pretrained/roberta-base/'
model = AutoModelForMaskedLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
fill_mask = pipeline('fill-mask', model=model, tokenizer=tokenizer)

# back-translation
trans = XunfeiApi()

res = fill_mask("Spend time online and odds are you'll have to type a username and password to check your e-mail, access your bank <mask> or read a newspaper story.    Enter Microsoft Corp...")
for answer in res:
    print(answer['token_str'])


origin_lang = 'zh'
temp_lang = 'ja'
text = "若打开IP白名单，则服务端会检查调用方IP是否在讯飞开放平台配置的IP白名单中，对于没有配置到白名单中的IP发来的请求，服务端会拒绝服务。"
res = trans(text, from_lang=origin_lang, to_lang=temp_lang)
print(res)
res = trans(res, from_lang=temp_lang, to_lang=origin_lang)
print(res)


