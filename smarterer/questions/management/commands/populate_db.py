from django.core.management.base import BaseCommand, CommandError
import csv
from questions.models import Question, Answer
from smarterer import settings


class Command(BaseCommand):
    help = 'Loads question data'
    csv_file = 'smarterer_code_challenge_question_dump.csv'

    def handle(self, *args, **options):

        Question.objects.all().delete()
        Answer.objects.all().delete()
        print('Deleted existing data')


        with open(settings.BASE_DIR + '/../' + self.csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            next(reader, None)
            for row in reader:

                q = Question(question=row[0])
                q.save()
                print('Saved question with id ' + str(q.id));

                a = Answer(question=q, choice=row[1], correct=True)
                a.save()

                for i in row[2].split(','):
                    aw = Answer(question=q, choice=i, correct=False)
                    aw.save()