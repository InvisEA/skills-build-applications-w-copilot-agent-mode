from datetime import timedelta
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import test_users, test_teams, test_activities, test_leaderboard, test_workouts

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Populate users
        for user_data in test_users:
            User.objects.create(**user_data)

        # Populate teams
        for team_data in test_teams:
            Team.objects.create(**team_data)

        # Populate activities
        for activity_data in test_activities:
            user = User.objects.get(username=activity_data.pop('username'))
            duration_str = activity_data.pop('duration')
            hours, minutes, seconds = map(int, duration_str.split(':'))
            activity_data['duration'] = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            Activity.objects.create(user=user, **activity_data)

        # Populate leaderboard
        for leaderboard_data in test_leaderboard:
            user = User.objects.get(username=leaderboard_data.pop('username'))
            Leaderboard.objects.create(user=user, **leaderboard_data)

        # Populate workouts
        for workout_data in test_workouts:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))