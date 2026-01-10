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

### 2.2 Klasy użytkowników

- **Administrator**:
  - Możliwość usuwania postów łamiących regulamin.
  - Zarządzanie użytkownikami, administrator posiada możliwość wyciszenia użytkownika na określony czas lub blokady jego konta.

### 2.3 Ograniczenia projektowe

#### 2.3.1 **Ograniczenia prawne**

**Ograniczenie:**  
System musi być zgodny z Rozporządzeniem o Ochronie Danych Osobowych (RODO), a wszystkie dane osobowe użytkowników muszą być fizycznie przechowywane na serwerach zlokalizowanych w granicach Europejskiego Obszaru Gospodarczego (EOG).

**Źródło:**  
Prawo Unii Europejskiej.

**Wpływ na architekturę systemu:**  
- Drastycznie zawęża wybór dostawców usług chmurowych do tych, którzy posiadają centra danych w EOG.
- Wymusza implementację mechanizmów do obsługi praw użytkowników (prawo do bycia zapomnianym, prawo do eksportu danych), co musi być uwzględnione w projekcie bazy danych i API.
- Narzuca konieczność anonimizacji danych w środowiskach deweloperskich i testowych.
- System umożliwia zmianę prywatności konta, przez co zdjęcia są widoczne tylko dla obserwujących (Privary by Design).

