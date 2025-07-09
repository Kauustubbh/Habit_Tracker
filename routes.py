from flask import Blueprint, render_template, request, redirect, url_for
import datetime
from collections import defaultdict

pages = Blueprint(
    "habits", __name__, template_folder="templates", static_folder="static"
    )
habits = ["Test habit", "Test 2"]
completions = defaultdict(list)


@pages.context_processor
def add_calc_date_range():
    def date_range(start: datetime.date):
        dates = [start + datetime.timedelta(days=diff) for diff in range(-3, 4)]
        return dates
    
    return {"date_range": date_range}


@pages.route("/")
def index():
    date_str = request.args.get("date")
    if date_str:
        selected_date = datetime.date.fromisoformat(date_str)
    else:
        selected_date = datetime.date.today()

    return render_template(
        "index.html", 
        title= "Habit Tracker - Home", 
        habits=habits, 
        selected_date=selected_date,
        completions=completions[selected_date]
    )

@pages.route("/add", methods=["GET", "POST"])
def add_habit():
    if request.method == "POST":
        habits.append(request.form.get("habit"))
    return render_template("add_habit.html", title="Habit Tracker - Add Habit", selected_date=datetime.date.today())


@pages.route("/complete", methods=["POST"])
def complete():
    date_sting = request.form.get("date")
    habit = request.form.get("habitName")
    date = datetime.date.fromisoformat(date_sting)
    completions[date].append(habit)

    return redirect(url_for(".index", date=date_sting))  #or habit.index

