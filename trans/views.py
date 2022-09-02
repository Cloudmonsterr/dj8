from django.shortcuts import render
import googletrans
from googletrans import Translator

# Create your views here.
def index(request):
    context = {
        'd' : googletrans.LANGUAGES,
        'bt' : 'ko',
        'at' : 'en'
    }
    if request.method == "POST":
        bt = request.POST.get('bt', "")
        word = request.POST.get('word', "")
        at = request.POST.get('at', "")
        translator = Translator()
        rt = translator.translate(word, src=bt, dest=at)
        context.update({
            'bt' : bt,
            'word' : word,
            'at' : at,
            'rt' : rt
        })
    return render(request, 'trans/index.html', context)




