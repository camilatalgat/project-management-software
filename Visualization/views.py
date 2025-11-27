# from django.shortcuts import render

# Create your views here.

# from django.shortcuts import render, get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.utils import timezone
# from datetime import timedelta
# from .models import Sprint, Task
# import json


# # API для данных графика
# class BurndownChartDataView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, sprint_id):
#         sprint = get_object_or_404(Sprint, id=sprint_id)
#         total_points = sprint.total_story_points or 0
#         days = (sprint.end_date - sprint.start_date).days + 1

#         ideal = []
#         actual = []
#         current_date = sprint.start_date

#         for day in range(days + 1):
#             date_str = current_date.strftime("%Y-%m-%d")

#             # Идеальная линия
#             ideal_points = max(0, total_points - (total_points * day / days))
#             ideal.append({"date": date_str, "points": round(ideal_points, 1)})

#             # Реальная линия
#             completed = Task.objects.filter(
#                 sprint=sprint,
#                 status='done',
#                 completed_at__date__lte=current_date
#             ).aggregate(total=models.Sum('story_points'))['total'] or 0

#             actual.append({"date": date_str, "points": total_points - completed})

#             current_date += timedelta(days=1)

#         return Response({
#             "ideal": ideal,
#             "actual": actual,
#             "sprint_name": sprint.name,
#             "total_points": total_points
#         })


# # Страница с графиком
# def burndown_chart_view(request, sprint_id):
#     sprint = get_object_or_404(Sprint, id=sprint_id)
#     return render(request, 'visualization/burndown_chart.html', {'sprint': sprint})



from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db import models  
from datetime import timedelta
from .models import Sprint
import json


def burndown_chart_view(request, sprint_id):
    sprint = get_object_or_404(Sprint, id=sprint_id)

    # Генерируем список всех дней спринта
    delta = sprint.end_date - sprint.start_date
    dates = [(sprint.start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]

    # Идеальная линия (прямая от total до 0)
    total_points = sprint.total_story_points
    ideal_burndown = []
    for i, date in enumerate(dates):
        remaining = total_points - (total_points * i / len(dates))
        ideal_burndown.append(round(remaining, 1))

    # Реальная линия — сколько поинтов осталось на каждый день
    actual_burndown = []
    for current_date in [sprint.start_date + timedelta(days=i) for i in range(delta.days + 1)]:
        # Считаем выполненные поинты до этой даты (включительно)
        completed_points = sprint.tasks.filter(
            status='done',
            completed_at__date__lte=current_date
        ).aggregate(total=models.Sum('story_points'))['total'] or 0

        remaining = total_points - completed_points
        actual_burndown.append(max(0, remaining))  # не ниже нуля

    context = {
        'sprint': sprint,
        'dates': json.dumps(dates),                    # ← важно: json.dumps!
        'ideal_burndown': json.dumps(ideal_burndown),  # ← важно: json.dumps!
        'actual_burndown': json.dumps(actual_burndown),# ← важно: json.dumps!
    }

    return render(request, 'visualization/burndown_chart.html', context)