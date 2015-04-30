from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Choice, Question
from .forms import QuestionForm


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class QuestionAddView(generic.CreateView):
    model = Question
    form_class = QuestionForm


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


def find_question(request):
    """
    SQL injection example

    :param request:
    :return:
    """
    question_text = request.POST.get('question_text', None)

    if question_text is None:
        return HttpResponseRedirect(reverse('polls:index'))

    qry = "SELECT * FROM polls_question WHERE question_text='%s'" % question_text
    try:
        question = Question.objects.raw(qry)[:1][0]
    except Question.DoesNotExist as e:
        raise Http404('Question does not exist!')

    print question

    return render(request, 'polls/detail.html', {'question': question})