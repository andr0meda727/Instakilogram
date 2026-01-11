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

cele biznesowe, cele uzytkownika i kpi??

### 1.3 Definicje, akronimy i skróty

- IK - instakilogram

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

#### 2.4.3 Założenia finansowe

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

### 3.1 Priorytetyzacja Wymagań

| ID         | Opis               | Korzyść | Kara | Koszt | Ryzyko | **Wynik** | **MVP** |
| :--------- | :----------------- | :-----: | :--: | :---: | :----: | :-------: | :-----: |
| **XXX-01** | vvvvvvvvvvvvvvvvvv |    0    |  0   |   0   |   0    |   **0**   |   ✅    |
| **XXX-02** | vvvvvvvvvvvvvvvvvv |    0    |  0   |   0   |   0    |   **0**   |   ✅    |
| **XXX-03** | vvvvvvvvvvvvvvvvvv |    0    |  0   |   0   |   0    |   **0**   |   ✅    |
| **XXX-04** | vvvvvvvvvvvvvvvvvv |    0    |  0   |   0   |   0    |   **0**   |   ✅    |
| **XXX-05** | vvvvvvvvvvvvvvvvvv |    0    |  0   |   0   |   0    |   **0**   |   ❌    |
