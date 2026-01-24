# Instakilogram

## 1. Wstęp

### 1.1 Cel

**Instakilogram**  
Aplikacja internetowa pozwalająca udostęniać zdjęcia oraz tworzyć sieć znajomych (wersja 1.0).  
Skupiamy się na eliminacji krótkich formatów wideo oraz szumu informacyjnego, pozwalająć użytkownikowi na kontrolę.

Poniższy dokument służy jako:

- Dokumentacja projektowa przeznaczona dla deweloperów.
- Kompendium wiedzy odnośnie projektu oraz przewodnik w szeroko pojętym modelowaniu oprogramowania.

### 1.2 Wizja, zakres i cele produktu

**Wizja**  
Aplikacja **maksymalnie** redukująca elementy rozpraszające występujące we współczesnych mediach społecznościowych.

**Zakres**  
Aplikacja udostępnia następujące funkcjonalności:

- Możliwość publikacji oraz zarządzania zdjęciami.
- Sieć znajomych, aplikacja umożliwia obserwację znajomych i interakcję z nimi poprzez komentarze i polubienia.
- System autentykacji.
- Chatowanie ze znajomymi z wykorzystaniem wbudowanego komunikatora.
- Publikowanie postów sponsorowanych przez firmy.
- Inteligetny system rekomendacji postów na podstawie zainteresowań użytkownika.

**Poza zakresem**  
Aplikacja nie będzie obsługiwać następujących funkcjonalności:

- Publikacja formatów wideo.
- System płatności dla firm chcących udostępnić post sponsorowany.
- Relacje (stories), które znikają po określonym czasie.
- Edycja zdjęć.

**Cele biznesowe:**

- vvvvvvvvvv
  - Kryterium akceptacji: vvv
- vvvvvvvvvv
  - Kryterium akceptacji: vvv

**Cele użytkownika:**

- vvvvvvvvvv
  - Kryterium akceptacji: vvv
- vvvvvvvvvv
  - Kryterium akceptacji: vvv

### 1.3 Definicje, akronimy i skróty

- **IK** - instakilogram
- **Post** - zdjęcie opublikowane przez użytkownika, mogące zawierać opis. Post może być skomentowany oraz polubiony przez innego użytkownika.

### 1.4 Przegląd dokumentu

## 2. Opis ogólny

### 2.1 Główne funkcje produktu

- **Wyświetlanie postów** Użytkownik może wyświetlić ostatnio dodane posty swoich znajomych.
- **Publikacja zdjęć** Użytkownik posiada możliwość dodania zdjęcia z opisem.
- **Zarządzanie zdjęciami** Użytkownik posiada możliwość usunięcia zdjęcia, jak i edycji jego opisu.
- **Komentarze** Użytkownik posiada możliwość komentowania opublikowanych zdjęć.
- **Sieć znajomych** Użytkownik posiada możliwość obserwacji swoich znajomych
- **Wyświetlanie postów znajomych** Po obserwacji użytkownik może wyświetlać posty znajomych na stronie głównej
- **Rekomendacja postów** Inteligentne algorytmy rekomendujące posty użytkownika tak, aby zmaksymalizować zainteresowanie użytkownika
- **Promowanie postów** W szczytowym zainteresowaniu algorytmy będą wyświetlać promowane posty, dostępne do wykupienia przez konta firmowe

### 2.2 Klasy użytkowników

- **Administrator**:
  - Możliwość usuwania postów łamiących regulamin.
  - Zarządzanie użytkownikami, administrator posiada możliwość wyciszenia użytkownika na określony czas lub blokady jego konta.

- **Konto firmowe**:
  - Możliwość dodania sponsorowanego posta.
  - Prosty panel do wyświetlenia statystyk danego posta.

- **Użytkownik**:
  - Wyświetlanie postów.
  - Publikacja zdjęć
  - Wyświetlanie profili
  - Funkcje społecznościowe takie jak budowanie sieci znajomych

### 2.3 Ograniczenia projektowe

#### 2.3.1 Ograniczenia prawne

- **Ograniczenie:**  
  System musi być zgodny z Rozporządzeniem o Ochronie Danych Osobowych (RODO), a wszystkie dane osobowe użytkowników muszą być fizycznie przechowywane na serwerach zlokalizowanych w granicach Europejskiego Obszaru Gospodarczego (EOG).

- **Źródło:**  
  Prawo Unii Europejskiej.

- **Wpływ na architekturę systemu:**
  - Drastycznie zawęża wybór dostawców usług chmurowych do tych, którzy posiadają centra danych w EOG.
  - Wymusza implementację mechanizmów do obsługi praw użytkowników (prawo do bycia zapomnianym, prawo do eksportu danych), co musi być uwzględnione w projekcie bazy danych i API.
  - Narzuca konieczność anonimizacji danych w środowiskach deweloperskich i testowych.
  - System umożliwia zmianę prywatności konta, przez co zdjęcia są widoczne tylko dla obserwujących (Privary by Design).

#### 2.3.2 Ograniczenia środowiskowe

- **Ograniczenie:**  
  System musi być zaprojektowany przy użyciu narzędzi i sposobów poznanych na uczelni. Spełniać założenia przedmiotu na którym będzie oceniany projekt

- **Źródło:**  
  Uczelnia

- **Wpływ na architekturę systemu:**
  - Ogranicza czas, który może zostać poświęcony na projektowanie systemu.
  - Zawęża funkcjonalności do najprostszych.
  - Narzuca pracę w 3-osobowym zespole studentów.

#### 2.3.3 Ograniczenie biznesowe

- **Ograniczenie:**  
  Infrastruktura powinna być maksymalnie tania, ale z możliwością skalowania, tak żeby do czasu pierwszych zysków z promowania postów nie wyczerpał się niewielki budżet

- **Źródło:**  
  Budżet przedsięwzięcia i ocena ryzyka

- **Wpływ na architekturę systemu:**
  - System budowany z myślą o chmurze
  - Wybór dostawców chmury zawężony do hyperscalerów którzy zapewnią skalowalność
  - Optymalizacja projektu pod kątem minimalizacji kosztów przetwarzania w chmurze

### 2.4 Założenia projektowe

#### 2.4.1 Założenia techniczne

- **Założenie:** Zakładamy wykorzystanie narzędzia [FFmpeg](ffmpeg.org) do standaryzacji szerokości zdjęć do 1080px oraz ich konwersji do formatu WebP z zachowaniem 80% jakości. Wnioskujemy, że pozwoli to na redukcję rozmiaru zdjęć o co najmniej 40%.
- **Ryzyko:** Przetwarzanie obrazów wymaga dużej mocy obliczeniowej procesora. Przy zwiększonej liczbie przesyłanych zdjęć, serwer może ulec przeciążeniu, co zwiększy czas odpowiedzi aplikacji lub doprowadzi do jej tymczasowej niedostępności.
- **Plan walidacji:**
  - **Co:** Przeprowadzenie testów wydajności procesu konwersji zdjęć.
  - **Jak:** Stworzenie skryptu testowego, który dokona konwersji 500 zdjęć - obserwacja obciążenia podczas tego procesu.
  - **Kiedy:** W trakcie implementacji funkcjonalności związanych z publikowaniem zdjęć.
  - **Kto:** Jeden z deweloperów.

#### 2.4.2 Założenia finansowe

- **Założenie:** Zakładamy, że projekt będzie realizowany przez studentów w ramach zajęć akademickich oraz utrzymywany na infrastrukturze chmurowej dostępnej w ramach bezpłatnej puli studenckiej Microsoft Azure. W związku z ograniczonym budżetem zakładamy wykorzystanie wyłącznie darmowych lub otwartoźródłowych narzędzi. Zakładamy, że taka konfiguracja będzie wystarczająca dla środowiska testowego i niewielkiej liczby użytkowników(pare studentów).
- **Ryzyko:** Ograniczone zasoby dostępne w darmowej puli Azure (moc obliczeniowa, pamięć RAM, transfer danych) mogą prowadzić do obniżonej wydajności systemu, dłuższych czasów odpowiedzi aplikacji. Istnieje również ryzyko przekroczenia limitów darmowego planu, co może spowodować wstrzymanie działania serwera lub naliczenie wysokich kosztów.
- **Plan walidacji:**
  - **Co:** Sprawdzenie wydajności aplikacji oraz zużycia zasobów w ramach darmowej puli Azure.
  - **Jak:** Uruchomienie aplikacji w docelowej konfiguracji i przeprowadzenie testów obciążeniowych, symulujących jednoczesne korzystanie z aplikacji przez 50–100 użytkowników. Monitorowanie zużycia CPU, pamięci RAM oraz transferu danych za pomocą Azure Monitor.
  - **Kiedy:** Po wdrożeniu pierwszej wersji aplikacji na środowisko testowe w chmurze.
  - **Kto:** Jeden z deweloperów.

#### 2.4.3 Założenia prawno-techniczne

- **Założenie:** Zakładamy że do moderacji treści wystarczy minimalistyczny sytem polegający na systemie zgłaszania niepoprawnych treści przez użytkowników.
- **Ryzyko:** Użytkownicy nie będą zgłaszać treści naruszających regulamin aplikacji, przez co platforma jest narażona na pociągnięcie do odpowiedzialności przez podmioty prawne.
- **Plan walidacji:**
  - **Co:** Badanie skuteczności wprowadzonego systemu
  - **Jak:** Badanie statystyczne zgłaszanych postów, ile zostało poprawnie zgłoszony ile false positive. Dodatkowo ankiety satysfakcji dla użytkowników
  - **Kiedy:** Pierwsze miesiące działalności
  - **Kto:** Zespół deweloperów

## 3. Wymagania funkcjonalne

**WF-01**

- **Tytuł:** Zarządzanie zdjęciami
- **Opis:** Umożliwia użytkownikom publikowanie zdjęć, jak i zarządzanie nimi (edycja, usuwanie).
- **Historyjka Użytkownika:**
  - Jako użytkownik,
  - chcę mieć możliwość publikacji, edycji opisu jak i usuwania zdjęć
  - abym mógł dzielić się swoimi chwilami z innymi.
- **Cel Biznesowy:** Udostępnienie platformy do dzielenia się zdjęciami z innymi użytkownikami
- **Warunki Wstępne:** Użytkownik jest zalogowany w aplikacji.
- **Warunki Końcowe:** Zdjęcie użytkownika zostaje opublikowane, oraz ma on możliwość edycji jego opisu, jak i usunięcia zdjęcia.
- **Kryteria Akceptacji:**
  - **WF-01-A: Pomyślne opublikowanie zdjęcia (Scenariusz Główny)**
    - _Opis:_ Zalogowany użytkownik próbuje opublikować zdjęcie
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Zrobiłem ciekawe zdjęcie i chcę je opublikować
      - **When:** Kliknę przycisk "Wstaw zdjęcie", wybiorę interesujące mnie zdjęcie oraz kliknę "Opublikuj".
      - **Then:** Dostanę informację o rozpoczętym procesie publikacji.
      - **And:** Post ze zdjęciem pojawi się na moim profilu.
      - **And:** Post ze zdjęciem wyświetli się na stronie głównej moich obserwujących.

  - **WF-01-B: Próba przesłania formatu wideo (Scenariusz Alternatywny)**
    - _Opis:_ Aplikacja uniemożliwia opublikowanie formatu wideo
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Nagrałem film oraz chcę go opublikować
      - **When:** Kliknę przycisk "Wstaw zdjęcie" oraz wybiorę nagrany film
      - **Then:** Przycisk "Opublikuj" pozostanie nieaktywny
      - **And:** Wyświetlony zostanie komunikat o braku możliwości publikacji formatów wideo

**WF-02**

- **Tytuł:** Zarządzanie reklamami oraz ich wyświetlanie użytkownikom
- **Opis:** Umożliwia reklamodawcom (konto firmowe) dodawanie reklam do systemu, a aplikacji wyświetlanie ich w formie niespersonalizowanych postów sponsorowanych oraz zliczanie ich wyświetleń.
- **Historyjka Użytkownika:**
  - Jako reklamodawca,
  - chcę mieć możliwość dodania reklamy do systemu oraz sprawdzenia jej statystyk,
  - aby móc promować swój biznes i ocenić skuteczność kampanii.
- **Cel Biznesowy:** Umożliwienie małym, lokalnym firmom taniej i prosto reklamować się w aplikacji oraz przetestowanie systemu reklamowego poprzez osiągnięcie założonej liczby wyświetleń.
- **Warunki Wstępne:** Użytkownik posiada konto firmowe oraz jest zalogowany do aplikacji.
- **Warunki Końcowe:** Reklama zostaje zapisana w systemie. Reklama jest wyświetlana użytkownikom na stronie głównej. System zlicza wyświetlenia reklamy.
- **Kryteria Akceptacji:**
  - **WF-02-A: Dodanie nowej reklamy (Scenariusz Główny)**
    - _Opis:_ Reklamodawca dodaje nową reklamę do systemu.
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowany na konto firmowe.
      - **And:** Mam przygotowaną treść reklamy (obraz + opis).
      - **When:** Przechodzę do panelu reklam, klikam „Dodaj reklamę”, wypełniam formularz i klikam „Zapisz”.
      - **Then:** Otrzymuję informację o poprawnym dodaniu reklamy.
      - **And:** Reklama pojawia się na liście aktywnych reklam.
      - **And:** Reklama może zostać wyświetlona użytkownikom na stronie głównej.
- **WF-02-B: Wyświetlenie reklamy użytkownikowi (Scenariusz Główny)**
  - _Opis:_ Uzytkownik widzi reklamy na stronie głównej.
  - _Kryteria Akceptacji:_
    - **Given:** Jestem zalogowany jako zwykły użytkownik.
    - **And:** Dostępne są posty na stronie głównej.
    - **When:** Przewijam kilka postó.
    - **Then:** Widzę post sponsorowany.
    - **And:** Post jest oznaczony jako sponsorowany.
- **WF-02-C: Wyświetlenie reklamy użytkownikowi (Scenariusz Główny)**
  - _Opis:_ Reklamodawca widzie swoje statystyki.
  - _Kryteria Akceptacji:_
    - **Given:** Jestem zalogowany na konto firmowe.
    - **And:** Dostępne są posty na stronie głównej.
    - **When:** Przewijam kilka postó.
    - **Then:** Widzę post sponsorowany.
    - **And:** Post jest oznaczony jako sponsorowany.

**WF-03**

- **Tytuł:** Rekomendacja postów
- **Opis:** Algorytmy serwujące użytkownikom kolejne posty wplatając od czasu do casu promowany post
- **Historyjka Użytkownika:**
  - Jako użytkownik,
  - Przegląda posty
  - Chce widzieć posty, które mu się spodobają
  - Od czasu do czasu zobaczy promowany post lub reklamę
- **Cel Biznesowy:** Sprzedaż promowanych postów oraz reklam
- **Warunki Wstępne:** Użytkownik jest zalogowany w aplikacji.
- **Warunki Końcowe:** Użytkownik kończy przeglądanie postów poprzez wyjście z aplikacji
- **Kryteria Akceptacji:**
  - **WF-03-A: Algorytm rekomenduje post (Scenariusz Główny)**
    - _Opis:_ Użytkownik przegląda sekcję postów
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Przeglądam posty
      - **When:** Przescrolluję w dół żeby zobaczyć następny post
      - **Then:** Algorytm wyświetli mi post który mi się spodoba, zostawię reakcję i przejdę dalej

  - **WF-03-B: Algorytm rekomenduje post promowany lub reklamę (Scenariusz Alternatywny)**
    - _Opis:_ W sekcji postów użytkownik widzi post promowany lub reklamę
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Przeglądam posty
      - **When:** Przescrolluję w dół żeby zobaczyć następny post
      - **Then:** Zostanie mi wyświetlony post promowany lub reklama która mnie zainteresuje
      - **And:** Kliknę w reklamę lub post promowany aby dowiedzieć się więcej

**WF-04**

- **Tytuł:** Sieć znajomych
- **Opis:** Umożliwia użytkownikom budowanie sieci znajomych poprzez obserwowanie innych kont
- **Historyjka Użytkownika:**
  - Jako użytkownik,
  - chcę mieć możliwość obserwacji mojego znajomego
  - abym mógł obserwować jego nowe posty ze zdjęciami
- **Cel Biznesowy:** Zwiększenie czasu spędzonego w aplikacji poprzez wyświetlanie użytkowonikom postów znajomych
- **Warunki Wstępne:** Użytkownik jest zalogowany w aplikacji.
- **Warunki Końcowe:** Użytkownik obserwuje wybrane konto i wyświetlane mu są posty na stronie głównej z obserwowanego konta
- **Kryteria Akceptacji:**
  - **WF-04-A: Obserwowanie użytkownika (Scenariusz Główny)**
    - _Opis:_ Zalogowany użytkownik próbuje obserwować wybrane konto
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Korzystam z wyszukiwarki i znajduję interesujące mnie konto po jego nazwie
      - **When:** Kliknę przycisk "Obserwuj" na wybranym koncie
      - **Then:** System dodaję wybrane konto do listy moich obserwowanych
      - **And:** Przycisk "Obserwuj" zmienia się na "Obserwujesz to konto"
      - **And:** Zdjęcia obserwowanej osoby pojawiają się na mojej stronie głównej

  - **WF-04-B: Odobserwowanie użytkownika (Scenariusz Alternatywny)**
    - _Opis:_ Zalogowany użytkownik chcę usunąć obserwację wybraego konta
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Korzystam z wyszukiwarki lub listy moich obserwowanych, aby wyszukać konto do odobserwowania
      - **When:** Kliknę przycisk "Obserwujesz to konto"
      - **Then:** Aplikacja wyświetli popup, w którym użytkownik będzie miał do wyboru opcję "Odobserwuj konto" lub "Anuluj"
      - **And:** Kliknę przycisk "Odobserwuj konto"
      - **And:** System usunie wybrane konto z moich obserwowanych
      - **And:** Posty od usuniętego konta nie będą się wyświetlać na stronie głównej w zakładce "Znajomi"

**WF-05**

- **Tytuł:** Interakcja z postami
- **Opis:** Umożliwia użytkownikom polubienie postów oraz ich komentowanie
- **Historyjka Użytkownika:**
  - Jako użytkownik,
  - chcę mieć możliwość polubienia postu oraz dodania komentarza
  - abym mógł wyrazić swoje zdanie na temat zdjęcia
- **Cel Biznesowy:** Zwiększenie wartości sieci znajomych poprzez budowanie więzi między użytkownikami przez interakcję
- **Warunki Wstępne:** Użytkownik jest zalogowany w aplikacji.
- **Warunki Końcowe:** Użytkownik polubił post oraz dodał komentarz, który jest widoczny dla innych użytkowników
- **Kryteria Akceptacji:**
  - **WF-05-A: Polubienie zdjęcia (Scenariusz Główny)**
    - _Opis:_ Zalogowany użytkownik próbuje polubić post
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Przeglądam posty na stronie głównej i znajduję ciekawe zdjęcie, które chcę polubić
      - **When:** Kliknę ikonę "Serca" na wybranym poście
      - **Then:** System zapisuję moje polubienie
      - **And:** Użytkownicy mogą zobaczyć kto polubił dany post

  - **WF-05-B: Skomentowanie zdjęcia (Scenariusz Alternatywny)**
    - _Opis:_ Zalogowany użytkownik chcę skomentować wybrany post
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Przeglądam posty na stronie głównej i znajduję ciekawe zdjęcie, które chcę skomentować
      - **When:** Kliknę ikonę "Komentarza" na wybranym poście
      - **Then:** Wyświetlą mi się aktualne komentarze innych użytkowników oraz na dole ekranu będe miał możliwość napisania komentarza
      - **And:** Napisałem komentarz i klikam przycisk "Skomentuj"
      - **And:** Użytkownicy mogą zobaczyć mój komenatrz

    - **WF-05-C: Usunięcie polubienia i komentarza (Scenariusz Alternatywny)**

    - _Opis:_ Zalogowany użytkownik chcę usunąć dodany komenatrz oraz polubienie
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem oraz skomentowałem i polubiłem post znajomego
      - **And:** Znajduję post, w którym chcę usunąć komentarz oraz polubienie
      - **When:** Kliknę podświetloną na czerwono ikonę "Serca" na wybranym poście oraz wejdę w komentarze i kliknę "Usuń" obok mojego komentarza
      - **Then:** System usunie mój komentarz oraz polubienie
      - **And:** Ikona "Serca" zmieni się ponownie na szarą, a komentarz zniknie
      - **And:** Użytkownicy nie widzą mojego polubienia ani komentarza

**WF-06**

- **Tytuł:** System autentykacji
- **Opis:** Umożliwia użytkownikom zakładanie konta i logowanie się do niego.
- **Historyjka Użytkownika:**
  - Jako nowy użytkownik,
  - chcę mieć możliwość rejestracji mojego konta
  - abym mógł wstawiać posty oraz mieć dostęp do aplikacji.
- **Cel Biznesowy:** Zwiększenie kontroli nad dostępem do aplikacji
- **Warunki Wstępne:** Użytkownik może wejść na stronę/aplikację i nie jest zalogowany/zarejestrowany.
- **Warunki Końcowe:** Konto zostaje utworzone lub dostaje informację o braku takiej możliwości
- **Kryteria Akceptacji:**
  - **WF-06-A: Pomyślne założenie konta (Scenariusz Główny)**
    - _Opis:_ Nowy użytkownik chce się zarejestrować
    - _Kryteria Akceptacji:_
      - **Given:** Nie posiadam konta
      - **And:** Wchodzę na stronę rejestracji
      - **When:** Kliknę przycisk "zarejestruj" po wypełnieniu danych
      - **Then:** System tworzy nowe konto
      - **And:** Dostaję informacje o pomyślnym zalogowaniu
      - **And:** Przekierowuje mnie do strony głównej

  - **WF-06-B: Próba założenia drugiego konta na ten sam e-mail (Scenariusz Alternatywny)**
    - _Opis:_ System blokuje tworzenie drugiego konta na ten sam adres e-mail
    - _Kryteria Akceptacji:_
      - **Given:** Jestem na ekranie rejestracji
      - **And:** Uzupełniam dane i wpisuję ten sam adres e-mail
      - **When:** Kliknę przycisk "zarejestruj" po wypełnieniu danych
      - **Then:** Konto nie zostanie utworzone
      - **And:** Dostanę informację, że taki e-mail jest zajęty

**WF-07**

- **Tytuł:** Zarządzanie kontem
- **Opis:** Dostosowywanie oraz personalizacja konta
- **Historyjka Użytkownika:**
  - Jako użytkownik,
  - Chce zmienić szczegóły swojego konta
- **Cel Biznesowy:** Zapewnienie klientom możliwości personalizacji i opcji zarządzania swoim kontem
- **Warunki Wstępne:** Użytkownik jest zalogowany w aplikacji.
- **Warunki Końcowe:** Użytkownik dostosowywuje swoje konto według swoich potrzeb
- **Kryteria Akceptacji:**
  - **WF-07-A: Użytkownik ustawia konto na prywatne (Scenariusz Główny)**
    - _Opis:_ Użytkownik wchodzi w sekcję ustawień
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Klikam przycisk zębatkę
      - **When:** Wybieram opcję "zmień prywatność konta"
      - **Then:** Prywatność konta się zmienia

  - **WF-07-B: Użytkownik zmienia zdjęcie profilowe oraz nazwę konta (Scenariusz Alternatywny)**
    - _Opis:_ Użytkownik chce spersonalizować swoje konto
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Klikam przycisk zębatkę
      - **When:** Wybieram opcję "personalizuj"
      - **Then:** Wyświetla się formularz personalizacji profilu
  - **WF-07-C: Użytkownik usuwa konto (Scenariusz Alternatywny)**
    - _Opis:_ Użytkownik chce usunąć swój profil
    - _Kryteria Akceptacji:_
      - **Given:** Jestem zalogowanym użytkownikiem
      - **And:** Klikam przycisk zębatkę
      - **When:** Wybieram opcję "usuń konto"
      - **Then:** Wyświetla się formularz usuwania profilu

### 3.1 Priorytetyzacja Wymagań

| ID        | Opis                                                     | Korzyść | Kara | Koszt | Ryzyko | **Wynik** | **MVP** |
| :-------- | :------------------------------------------------------- | :-----: | :--: | :---: | :----: | :-------: | :-----: |
| **WF-01** | Zarządzanie zdjęciami                                    |   21    |  21  |  13   |   5    | **2,33**  |   ✅    |
| **WF-02** | Zarządzanie reklamami oraz ich wyświetlanie użytkownikom |    5    |  8   |   3   |   3    | **2,16**  |   ✅    |
| **WF-03** | Rekomendacja postów                                      |   13    |  5   |   8   |   13   | **0,86**  |   ❌    |
| **WF-04** | Sieć znajomych                                           |   21    |  21  |   8   |   8    | **2,63**  |   ✅    |
| **WF-05** | Interakcja z postami                                     |    8    |  5   |   2   |   3    |  **2,6**  |   ✅    |
| **WF-06** | System autentykacji                                      |   21    |  21  |   3   |   13   | **2,33**  |   ✅    |
| **WF-07** | Zarządzanie kontem                                       |    8    |  13  |   3   |   5    | **2,63**  |   ✅    |
| **WF-07** | Chat                                                     |    3    |  3   |  21   |   13   | **0,18**  |   ❌    |

## 4. Atrybuty jakościowe

Atrybuty jakościowe definiują, jak dobrze system ma działać. Wpłwają one na zadowolenie użytkowników, co jest kluczowe w aplikacjach społecznośniowych, takich jak **IK**.

### 4.1 Priorytetyzacja Wymagań

| Atrybut Jakościowy      | Opis                                                                  | Uzasadnienie                                                                                                                                                                                                                                                            |
| :---------------------- | :-------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Użyteczność**         | Jak łatwo korzysta się z aplikacji?                                   | Aplikacja powinna być intuicyjna, żeby nie odstraszać użytkowników skomplikowanym interfejsem.                                                                                                                                                                          |
| **Wieloplatformowość**  | Jak aplikacja działa na różnych systemach operacyjnych?               | IK musi posiadać aplikacje natywne na urządzenia mobilne, żeby zachęcić użytkowników do korzystania z niej. Większość użytkowników korzysta z socialmediów z telefonów.                                                                                                 |
| **Niezawodność**        | Jak często system jest dostępny i działa poprawnie? (np. 99.9% czasu) | Uptime 95% lub więcej, zwłaszcza na początku działalności. Jesteśmy nastawieni na konkretny rynek (Polska), przez co możemy sobie pozwolić na przerwy techniczne w nocy.                                                                                                |
| **Wydajność**           | Jak szybko system odpowiada na żądania w określonych warunkach?       | Działanie natychmiastowe nie jest kluczowym priorytem, nie chcemy żeby użytkownicy musieli czekać aż załadują się nowe zdjęcia, ale nie potrzebujemy minimalnych opoźnień.                                                                                              |
| **Bezpieczeństwo**      | Jak aplikacja chroni prywatność i dane użytkowników?                  | Użytkownicy mają możliwość ustawienia profilu na prywatny, co pozwala dzielić się im swoimi zdjęciami tylko z obserwującymi. Istotne jest, żeby nie było żadnych luk w bezpieczeństwie, które pozwolą na niekontrolowany dostęp do owych zdjęć, jak i danych logowania. |
| **Obserwowalność**      | Jak łatwo można monitorować statystyki?                               | Monitorowanie metryk takich jak wyświetlenia, polubienia, komentarze oraz zaangażowanie będzie istotne dla klientów biznesowych, chcących reklamować swoje usługi.                                                                                                      |
| **Rozszerzalność**      | Jak łatwo będzie rozszerzać aplikacje o kolejne funkcjonalności?      | Dodawanie nowych funkcjonalności nie będzie naszym priorytetem, ze względu na to, że chcemy ograniczać niepotrzebne funkcje (niski)                                                                                                                                     |
| **Internacjonalizacja** | Jak aplikacja rozwiązuje problem użytkowników z różnych krajów?       | Wprowadzenie kilku języków nie jest wymagane do podstawowego działania aplikacji w Polsce. Przyszłościowo można dodać opcje tłumaczenia, żeby wyjść na rynek zagraniczny                                                                                                |

### 4.2 Mierzalna specyfikacja

**Scenariusz 1: Użyteczność**

| Element           | Opis                                                                                                                                      |
| :---------------- | :---------------------------------------------------------------------------------------------------------------------------------------- |
| **Źródło bodźca** | Użytkownik                                                                                                                                |
| **Bodziec**       | Próbuje opublikować pierwsze zdjęcie oraz krótki opis                                                                                     |
| **Artefakt**      | Interfejs użytkownika - publikacja postów                                                                                                 |
| **Środowisko**    | Użytkownik uruchamia aplikację pierwszy raz                                                                                               |
| **Reakcja**       | System prosi użytkownika o zalogowanie się na konto, a następnie prowadzi go przez proces publikacji postu (wybór zdjęcia, dodanie opisu) |
| **Miara reakcji** | Czas potrzebny do opublikowania zdjęcia po założeniu konta powinien wynieść poniżej 1 minuty.                                             |

**Scenariusz 3: Niezawodność**

| Element           | Opis       |
| :---------------- | :--------------------------------------------------------------- |
| **Źródło bodźca** | Awaria backendu / Przeciążenie serwerów |
| **Bodziec**       | Serwer przestaje odpowiadać na żądania (timeout > 5s) |
| **Artefakt**      | Baza danych lub serwery aplikacji |
| **Środowisko**    | Normalny ruch użytkowników, główny serwer niedostępny |
| **Reakcja**       | Aplikacja wykrywa awarię i przekierowuje żądania do serwera zastępczego w ciągu 15s |
| **Miara reakcji** | Uptime ≥ 95% w skali miesiąca; MTTR < 15 minut; max 2 minuty niedostępności dla użytkownika |


### 4.3 Analiza kompromisów architektonicznych

**4.3.1 Użyteczność**

- **Cel:** Osiągnięcie czasu publikacji zdjęcia przez nowych użytkowników poniżej 1 minuty.
- **Możliwe rozwiązanie architektoniczne:** Zaprojektowanie interfejsu w taki sposób, aby w widoku publikacji zdjęcia były zawarte tylko najważniejsze informacje, a zaawansowane opcje były ukryte pod ikoną zębatki.
- **Kompromis:**
  - **Pozytywny:**
    - Interfejs dla użytkowników korzystających z aplikacji pierwszy raz jest czytelny i intuicyjny.
    - Proces publikacji jest prosty, co powinno zwiększyć liczbę postów w aplikacji.
  - **Negatywny:**
    - Użytkownicy wymagający bardziej zaawansowanych opcji mogą mieć problem z ich znalezieniem.
    - Zwiększamy czas potrzebny do implementacji poprzez research upodobań użytkowników.

**4.3.3 Niezawodność**

- **Cel:** Uptime ≥ 95% w skali miesiąca; MTTR < 15 minut; max 2 minuty niedostępności dla użytkownika
- **Możliwe rozwiązanie architektoniczne:** Replikacja bazy danych master-slave, kolejkowanie żądań, system automatycznego wykrywania awarii
- **Kompromis:**
  - **Pozytywny:**
    - Ciągłość działania w przypadku awarii pojedynczych modułów
    - Możliwe przeprowadzanie przerw technicznych na pojedynczych serwerach bez wpływu na użytkowników
  - **Negatywny:**
    - Wzrost kosztów chumry w związku z potrzebą utrzymania nowych serwerów
    - Większa złożoność systemu która utrudni debugowanie i zwiększy czas wdrażania nowych rozwiązań
    

## 5. Odkrywanie i Analiza Wymagań

### 5.1 Analiza Porównawcza

Porównanie aplikacji IK z najlepszymi praktykami rynkowymi w celu identyfikacji mocnych i słabych stron oraz znalezienia inspiracji do ulepszeń.

- **Identyfikacja Konkurencji/Wzorców:** Podmioty rozwiązujące podobny problem
  - _Konkurencja bezpośrednia:_
    - **Instagram** - największa platforma społecznościowa do udostępnienia zdjęć oraz filmów
    - **BeReal** - aplikacja, która zachęca użytkowników do dzielenia się nieedytowanymi zdjęciami pokazującymi rzeczywistość
  - _Konkurencja pośrednia:_
    - **XYZ** - vvvvvvvvvvvvvvvvvv
  - _Wzorce funkcjonalne:_
    - **XYZ** - vvvvvvvvvvvvvvvvvv

- **Zdefiniowanie Kryteriów Oceny:** Tabela z kryteriami obejmującymi kluczowe aspekty, takie jak funkcjonalność, user experience (UX), model biznesowy i wsparcie.
  | Kryterium | Opis kryterium | Instakilogram | Instagram | BeReal |
  | :---------------------- | :-------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------- | :-------------------------------------------------------------------- |
  | **Dostępne formaty do publikacji** | Co można opublikować na platformie? | IK | IG | BeReal |
  | **Inteligentne rekomendacje** | Sposób działania systemu rekomendacji postów | IK | IG | BeReal |
  | **User experience** | Intuicyjność korzystania z aplikacji | IK | IG | BeReal |
  | **Model biznesowy** | vvvvvvv | IK | IG | BeReal |
  | **Wsparcie** | Dostępność wsparcia dla użytkowników | IK | IG | BeReal |

- **Synteza Wyników:** Co konkurencja robi dobrze? Gdzie są ich słabe punkty? Jakie unikalne funkcje oferują?
