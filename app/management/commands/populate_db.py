# management/commands/populate_db.py
# Uruchom: python manage.py populate_db

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from app.models import Post, Like, Friendship
import random
from datetime import datetime, timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Wypełnia bazę danych przykładowymi danymi'

    def handle(self, *args, **kwargs):
        # Wyczyść bazę
        User.objects.all().delete()
        
        self.stdout.write('Tworzenie użytkowników...')
        
        # Twórz użytkowników
        users_data = [
            {'username': 'anna_kowalska', 'bio': 'Fotografka z Krakowa ', 'email': 'anna@example.com'},
            {'username': 'jan_nowak', 'bio': 'Podróżnik i bloger ', 'email': 'jan@example.com'},
            {'username': 'maria_wisniowska', 'bio': 'Miłośniczka kotów ', 'email': 'maria@example.com'},
            {'username': 'piotr_kaminski', 'bio': 'Developer & Gamer ', 'email': 'piotr@example.com'},
            {'username': 'katarzyna_lewandowska', 'bio': 'Foodie | Warszawa ', 'email': 'kasia@example.com'},
            {'username': 'tomasz_wojcik', 'bio': 'Fitness &健康 ', 'email': 'tomasz@example.com'},
            {'username': 'magdalena_kozlowska', 'bio': 'Artist ', 'email': 'magda@example.com'},
            {'username': 'lukasz_jankowski', 'bio': 'Muzyk | DJ ', 'email': 'lukasz@example.com'},
            {'username': 'agnieszka_wojciechowska', 'bio': 'Book lover ', 'email': 'aga@example.com'},
            {'username': 'marcin_krawczyk', 'bio': 'Nature photographer ', 'email': 'marcin@example.com'},
        ]
        
        users = []
        for i, data in enumerate(users_data):
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password='password123',
                bio=data['bio'],
                profile_picture=f'https://i.pravatar.cc/150?u={data["username"]}'
            )
            # Pierwszy użytkownik (anna_kowalska) jako staff
            if i == 0:
                user.is_staff = True
                user.is_superuser = True
                user.save()
            users.append(user)
        
        self.stdout.write(f'✓ Utworzono {len(users)} użytkowników')
        
        # Twórz znajomości
        self.stdout.write('Tworzenie znajomości...')
        main_user = users[0]  # anna_kowalska jako główny użytkownik
        
        # Anna ma znajomych: Jan, Maria, Piotr, Katarzyna
        friends_of_main = users[1:5]
        for friend in friends_of_main:
            Friendship.objects.create(user=main_user, friend=friend)
            Friendship.objects.create(user=friend, friend=main_user)
        
        # Inne losowe znajomości
        for _ in range(15):
            user1, user2 = random.sample(users, 2)
            if not Friendship.objects.filter(user=user1, friend=user2).exists():
                Friendship.objects.create(user=user1, friend=user2)
                Friendship.objects.create(user=user2, friend=user1)
        
        total_friendships = Friendship.objects.count() // 2
        self.stdout.write(f'✓ Utworzono {total_friendships} znajomości')
        
        # Twórz posty
        self.stdout.write('Tworzenie postów...')
        
        captions = [
            'Piękny dzień! ',
            'Nowe miejsce do odkrycia ',
            'Smacznego! ',
            'Zachód słońca nad morzem ',
            'Kocham to miejsce ',
            'Weekend vibes ',
            'Nowy projekt w trakcie ',
            'Treningowy dzień ',
            'Czas na kawę ',
            'Przygoda trwa! ',
            'Relaks ',
            'Z przyjaciółmi ',
            'Moje ulubione ',
            'Inspiracja dnia ',
            'Natura jest piękna ',
        ]
        
        posts = []
        for user in users:
            num_posts = random.randint(3, 8)
            for i in range(num_posts):
                days_ago = random.randint(0, 30)
                post = Post.objects.create(
                    user=user,
                    image_url=f'https://picsum.photos/600/600?random={user.id}{i}',
                    caption=random.choice(captions),
                    created_at=datetime.now() - timedelta(days=days_ago)
                )
                posts.append(post)
        
        self.stdout.write(f'✓ Utworzono {len(posts)} postów')
        
        # Twórz polubienia
        self.stdout.write('Tworzenie polubień...')
        
        likes_count = 0
        for post in posts:
            # Każdy post ma losową liczbę polubień (0-7 użytkowników)
            num_likes = random.randint(0, 7)
            likers = random.sample(users, num_likes)
            
            for liker in likers:
                if liker != post.user:  # Użytkownik nie lajkuje własnych postów
                    Like.objects.create(user=liker, post=post)
                    likes_count += 1
        
        # Anna (main user) lubi konkretne posty
        main_user_likes = random.sample([p for p in posts if p.user != main_user], 15)
        for post in main_user_likes:
            Like.objects.get_or_create(user=main_user, post=post)
            likes_count += 1
        
        self.stdout.write(f'✓ Utworzono {likes_count} polubień')
        
        self.stdout.write(self.style.SUCCESS('\n=== Baza danych wypełniona! ==='))
        self.stdout.write(f'Użytkowników: {User.objects.count()}')
        self.stdout.write(f'Postów: {Post.objects.count()}')
        self.stdout.write(f'Znajomości: {Friendship.objects.count() // 2}')
        self.stdout.write(f'Polubień: {Like.objects.count()}')
        self.stdout.write(f'\nGłówny użytkownik do testów:')
        self.stdout.write(f'  Username: anna_kowalska')
        self.stdout.write(f'  Password: password123')