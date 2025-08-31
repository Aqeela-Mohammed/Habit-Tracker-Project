#Final Complete Habit Tracker Project

#Features:

#- Habit tracking with streaks

#- JSON data storage

#- Functional programming (map, filter, reduce)

#- Weekly reports

#- Default pre-filled habits

#- Docstrings for all classes/methods

#- Unit test included

#- User interface via menu

#- Clear screen functionality

import json
import os
import datetime
from functools import reduce
import time


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


class Habit:
    """
    Represents a habit with tracking data like name, frequency, and streaks.
    """

    def __init__(self, name, frequency, start_date=None, dates_done=None, streaks=None):
        self.name = name
        self.frequency = frequency  # 'daily' or 'weekly'
        self.start_date = start_date or str(datetime.date.today())
        self.dates_done = dates_done or []
        self.streaks = streaks or []

    def mark_done(self, date=None):
        """mark today (or given date) as done"""
        today = date or str(datetime.date.today())
        try:
            # Check if date is in correct format
            datetime.datetime.strptime(today, "%Y-%m-%d")
        except ValueError:
            print(f"Error: Invalid date format for {today}. Use 'YYYY-MM-DD'.")
            return

        if today in self.dates_done:
            print(f"Bruh...({self.name})already done for today {today}🤦‍\nGo chill, no double credit😂.")
            return

        self.dates_done.append(today)
        self.dates_done.sort()  # Sort to ensure correct order
        if not self.streaks:
            self.streaks.append(1)  # Start first streak
            print(f'🔥First streak for {self.name} !')
        else:
            if len(self.dates_done) == 1:  # Only one completion
                self.streaks.append(1)  # Start new streak
            else:
                try:
                    # Calculate gap between last two dates
                    last_date = datetime.datetime.strptime(self.dates_done[-2], "%Y-%m-%d").date()
                    today_date = datetime.datetime.strptime(today, "%Y-%m-%d").date()
                    gap = (today_date - last_date).days
                    if self.frequency == 'daily':
                        if gap == 1:
                            self.streaks[-1] += 1  # Continue streak
                            print(f'✅Nice! streak for {self.name} is now {self.streaks[-1]} days!')
                            if self.streaks[-1]==7:
                                print('1.Week straight 🌟 keep flexing💪')
                            elif self.streaks[-1]==30:
                                print('30 days!? ok calm down champ😅')
                        else:
                            self.streaks.append(1)  # Start new streak
                            print(f"🙃Oops streak broke! new streak for {self.name} started")
                            print ('Do not worry, happens to the best of us😉')
                            #reset again .....story of my life😅
                            print("Awesome work! Keep it up!")
                    elif self.frequency == 'weekly':
                        if gap == 7:
                            self.streaks[-1] += 1
                            print(f"✅Weekly streak for{self.name} : {self.streaks[-1]} weeks!🔥")
                        else:
                            self.streaks.append(1)
                            print(f"Started a new weekly streak for {self.name}️🌟!")
                except (IndexError, ValueError):
                    self.streaks.append(1)
                    print(f"🤷‍♀️New streak started for {self.name}")


    def current_streak(self):
        return self.streaks[-1] if self.streaks else 0

    def max_streak(self):
        return max(self.streaks) if self.streaks else 0

    def to_dict(self):
         """convert habit to dict for JSON saving."""
         return {
                'name': self.name,
                'frequency': self.frequency,
                'start_date': self.start_date,
                'dates_done': self.dates_done,
                'streaks': self.streaks }


    @staticmethod
    def from_dict(data):
        """create Habit object from dict."""
        return Habit(
                name=data['name'],
                frequency=data['frequency'],
                start_date=data['start_date'],
                dates_done=data['dates_done'],
                streaks=data['streaks']
            )

class HabitManager:
    """
    Manages a collection of habits, including saving/loading and analytics.
    """
    def __init__(self):
        self.habits = []
        self.file_name = "habits_data.json"
        self.load_data()
        if not self.habits:
            self.add_default_habits()

    def add_default_habits(self):
        """Add 5 sample habits with 4 weeks of predefined data."""
        default = [
        # Daily habit with 28 days in a row
        Habit("Drink Water", "daily", start_date="2025-07-29",
                       dates_done=[
                           "2025-07-29", "2025-07-30", "2025-07-31",
                           "2025-08-01", "2025-08-02", "2025-08-03", "2025-08-04",
                           "2025-08-05", "2025-08-06", "2025-08-07",
                           "2025-08-08", "2025-08-09", "2025-08-10", "2025-08-11",
                           "2025-08-12", "2025-08-13", "2025-08-14", "2025-08-15",
                           "2025-08-16", "2025-08-17", "2025-08-18", "2025-08-19",
                           "2025-08-20", "2025-08-21", "2025-08-22", "2025-08-23",
                           "2025-08-24", "2025-08-25"
                       ],
                       streaks=[28]),

         #Weekly habit (every 7 days)
        Habit("Exercise", "weekly", start_date="2025-07-29",
                       dates_done=["2025-07-29", "2025-08-05", "2025-08-12", "2025-08-19", "2025-08-26"],
                       streaks=[5]),

         # Daily reading habit, completed almost daily but missed a few days
        Habit("Read Book", "daily", start_date="2025-07-29",
                       dates_done=[
                           "2025-07-29", "2025-07-30", "2025-07-31",
                           "2025-08-01", "2025-08-02", "2025-08-03", "2025-08-04",
                           "2025-08-06", "2025-08-07", "2025-08-08",
                           "2025-08-09", "2025-08-11", "2025-08-12",
                           "2025-08-14", "2025-08-15", "2025-08-16",
                           "2025-08-18", "2025-08-19", "2025-08-20", "2025-08-22",
                           "2025-08-23", "2025-08-24", "2025-08-25"
                       ],
                       streaks=[7, 4, 5, 7]),

         # Meditation daily but less consistent
        Habit("Meditate", "daily", start_date="2025-07-29",
                       dates_done=[
                           "2025-07-29", "2025-07-30",
                           "2025-08-02", "2025-08-03",
                           "2025-08-07", "2025-08-08",
                           "2025-08-12", "2025-08-13",
                           "2025-08-18", "2025-08-19", "2025-08-24", "2025-08-25"
                       ],
                       streaks=[2, 2, 2, 2, 2, 2]),

         # Weekly cleaning habit
        Habit("Clean Room", "weekly", start_date="2025-07-29",
                       dates_done=["2025-07-29", "2025-08-05", "2025-08-12", "2025-08-19"],
                       streaks=[4])
             ]
        self.habits.extend(default)
        self.save_data()
    def add_habit(self):

         """add new habit from user input."""
         while True:

            name = input("Enter habit name (or 'cancel' to exit): ").strip()
            if name.lower() == 'cancel':
                return
            if any(h.name.lower() == name.lower() for h in self.habits):
                return print(f"Habit {name} already exists.")
            frequency = input("Enter frequency (daily/weekly): ").strip().lower()
            if frequency in ['daily', 'weekly']:
                new_habit = Habit(name=name, frequency=frequency)
                self.habits.append(new_habit)
                self.save_data()
                print(f"Habit '{name}' added successfully!")
                break
            else:
                print("Invalid frequency. Please enter 'daily' or 'weekly'.")

    def delete_habit(self):

        self.display_habits()
        name = input("Enter habit name to delete (or 'cancel' to exit): ").strip()
        time.sleep(0.1)
        if not any(h.name.lower() == name.lower() for h in self.habits):
            return print(f'Habit "{name}" not found. Try again.')
        if name.lower() == 'cancel':
            return
        self.habits = [h for h in self.habits if h.name.lower() != name.lower()]
        if any(h.name.lower() == name.lower() for h in self.habits):
            print(f'Error: Failed to delete "{name}". Please try again.')
        else:
            self.save_data()
            print(f"Habit '{name}' deleted successfully!")

    def mark_habit_done(self):
        self.display_habits()
        name = input("Enter habit name to mark done (or 'cancel' to exit): ").strip()
        if name.lower() == 'cancel':
            return
        for habit in self.habits:
            if habit.name.lower() == name.lower():
                habit.mark_done()
                self.save_data()
                return
        print(f"Habit '{name}' not found.")

    def display_habits(self):
        """display all habits in a table format."""
        if not self.habits:
            print("No habits found.")
            return
        print(f"\n{'Habit':<20} {'Type':<10} {'Current':<10} {'Max':<10}")
        print("-" * 50)
        for h in self.habits:
            print(f"{h.name:<20} {h.frequency:<10} {h.current_streak():<10} {h.max_streak():<10}")

    def weekly_report(self):
        """show completion in last 7 days."""
        today = datetime.date.today()
        week_ago = today - datetime.timedelta(days=7)
        print("\nWeekly Report (Last 7 days)")
        print("-" * 40)
        for h in self.habits:
            count = len([d for d in h.dates_done if datetime.datetime.strptime(d, "%Y-%m-%d").date() >= week_ago])
            print(f"{h.name:<20}: {count} times")
            # wow some one is actually consistent👀

    def most_consistent_habit(self):
        """Return the habit with the longest streak."""
        if not self.habits:
            print("No habits found.")
            return
        best = max(self.habits, key=lambda h: h.max_streak())
        print(f"\nMost consistent habit: {best.name} with a max streak of {best.max_streak()}")

    def least_consistent_habit(self):
        """Return the habit with the lowest streak (but at least 1)."""
        if not self.habits:
            print("No habits found.")
            return
        worst = min(self.habits, key=lambda h: h.max_streak() if h.max_streak() > 0 else float('inf'))
        if worst.max_streak() == 0:
            print("\nNo completed habits yet.")
        else:
            print(f"\nLeast consistent habit: {worst.name} with a max streak of {worst.max_streak()}")

    def save_data(self):
        """save all habits to JSON file."""
        try:
            with open(self.file_name, "w") as f:
                json.dump([h.to_dict() for h in self.habits], f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        """load habits from JSON file."""
        try:
             if os.path.exists(self.file_name):
                 with open(self.file_name, "r") as f:
                     data = json.load(f)
                     self.habits = list(map(Habit.from_dict, data))
        except json.JSONDecodeError:
            print("Error: Corrupted JSON file. Starting with empty habits.")
            self.habits = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self.habits = []

# Functional programming examples
def get_daily_habits(manager):
    """return all daily habits(example of filter)."""
    return list(filter(lambda h: h.frequency == 'daily', manager.habits))

def get_max_streak(manager):
     """return max streak using reduce (example of fp)."""
     return reduce(lambda x, y: max(x, y), [h.max_streak() for h in manager.hapits],0)
#I have no idea why this works but it does
def find_max_streak(manager):
    """simple loop version for max streak."""
    max_streak=0
    for h in manager.hapits:
        if h.max_streak() > max_streak:
            max_streak = h.max_streak()
    return max_streak
# Unit tests
def test_streak_logic():
    """Test streak update logic for daily habit."""
    test_habit = Habit("Test", "daily", dates_done=["2025-07-18", "2025-07-19"], streaks=[2])
    test_habit.mark_done(date="2025-07-20")
    assert test_habit.current_streak() == 3
    print("✅ Streak logic test passed.")

def test_weekly_streak():
    """Test streak update logic for weekly habit."""
    test_habit = Habit("TestWeekly", "weekly", dates_done=["2025-07-06", "2025-07-13"], streaks=[2])
    test_habit.mark_done(date="2025-07-20")
    assert test_habit.current_streak() == 3
    print("✅ Weekly streak test passed.")

def test_same_day_completion():
    """Test marking habit as done twice on the same day."""
    test_habit = Habit("TestSameDay", "daily", dates_done=["2025-07-20"], streaks=[1])
    test_habit.mark_done(date="2025-07-20")
    assert test_habit.current_streak() == 1
    assert len(test_habit.dates_done) == 1
    print("✅ Same day completion test passed.")

def test_habit_creation():
    """Test creating a new habit."""
    manager = HabitManager()
    old_count = len(manager.habits)
    manager.habits.append(Habit("NewHabit", "daily"))
    assert len(manager.habits) == old_count + 1
    print("✅ Habit creation test passed.")

def test_habit_deletion():
    """Test deleting a habit."""
    manager = HabitManager()
    manager.habits.append(Habit("TempHabit", "daily"))
    manager.habits = [h for h in manager.habits if h.name != "TempHabit"]
    assert not any(h.name == "TempHabit" for h in manager.habits)
    print("✅ Habit deletion test passed.")

 # Main menu
def main():
    """main menu loop"""
    manager = HabitManager()

    while True:
        clear_screen()
        time.sleep(0.5)
        print("\n==== Habit Tracker ====\n")
        print("1. View Habits📋")
        print("2. Add New Habit➕")
        print("3. Delete Habit❌")
        print("4. Mark Habit as Done☑️")
        print("5. Weekly Report📊")
        print("6. Run Tests⚗️")
        print("7. View Daily Habits🌞")
        print("8. View Max Streak🎇")
        print("9. Most Consistent Habit🤩")
        print("10. Least Consistent Habit🥲")
        print("11. Exit 👋")
        choice = input("\nSelect an option: ")
        time.sleep(0.5)
        if choice == '1':
            clear_screen()
            manager.display_habits()
            input("\nPress Enter to return...")
        elif choice == '2':
            clear_screen()
            manager.add_habit()
            input("\nPress Enter to return...")
        elif choice == '3':
            clear_screen()
            manager.delete_habit()
            input("\nPress Enter to return...")
        elif choice == '4':
            clear_screen()
            manager.mark_habit_done()
            input("\nPress Enter to return...")
        elif choice == '5':
            clear_screen()
            manager.weekly_report()
            input("\nPress Enter to return...")
        elif choice == '6':
            clear_screen()
            test_streak_logic()
            test_weekly_streak()
            test_same_day_completion()
            test_habit_creation()
            test_habit_deletion()
            input('\n Tests completed. Press Enter to return...')
        elif choice == '7':
            clear_screen()
            daily_habits = get_daily_habits(manager)
            if daily_habits:
                print("\nDaily Habits:")
                for h in daily_habits:
                    print(f"- {h.name}")
            else:
                print("No daily habits found.")
            input("\nPress Enter to return...")
        elif choice == '8':
            clear_screen()
            max_streak = find_max_streak(manager)
            print(f"\nMax streak across all habits: {max_streak}")
            input("\nPress Enter to return...")
        elif choice == '9':
            clear_screen()
            manager.most_consistent_habit()
            input("\nPress Enter to return...")
        elif choice == '10':
            clear_screen()
            manager.least_consistent_habit()
            input("\nPress Enter to return...")
        elif choice == '11':
            print("Exiting. Bye!")
            break
        else:
            print("Invalid choice. Try again.")
            input("\nPress Enter to return...")

if __name__ == "__main__":
    main()