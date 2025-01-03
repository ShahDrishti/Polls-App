from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from django.template import loader
from django.db.models import F
from django.urls import reverse
from django.views import generic

from django.utils import timezone


from .models import Choice,Question

#GENERIC VIEWS
class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
class DetailView(generic.DetailView):
    model= Question
    template_name ="polls/detail.html"
    context_object_name="question"
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Explicitly add choices to the context
        context['choices'] = self.object.choice_set.all()
        return context

class ResultsView(generic.DetailView):
    model=Question
    template_name="polls/results.html"





#VEWS AS FUNCTIONS 
# def index(request):
#     #return HttpResponse("Hello , world. You're at the polls index.")
#     latest_question_list= Question.objects.order_by("pub_date")[:3]
#     template =loader.get_template("polls/index.html")
#     context={
#         "latest_question_list": latest_question_list,
#     }
#     return HttpResponse(template.render(context,request))
# def detail(request , question_id):
#     question = get_object_or_404(Question , pk=question_id)
#     print("question :" ,question)
#     print("Choices",question.choice_set.all())
#     return render(request,"polls/detail.html",{"question":  question})

# def results(request , question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request,"polls/results.html",{"question":question})
def vote(request, question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice =question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question":question,
                "error_message": "You didn't select a choice .",
            },
        )
    else:
        selected_choice.votes =F("votes")+1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))
