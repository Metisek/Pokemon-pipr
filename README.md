# Pokemon - Projekt PIPR 2022



## Wstęp

Projekt stanowi symulator walk pokemonów korzystając z danych dołączonych do zadania (znajdujacych się w katalogu "reference"), przekonwertowanych na plik JSON.

Program umożliwia grę dwóch użytkowników i grę przeciwko komputerowi który wykonuje logiczne ruchy zgodnie z algorytmem ataków. Walka odbywa się jak w oryginalnej serii gier pokemon - po kolei, w każdej rundzie oba pokemony obydwu graczy walczą ze sobą 1vs1, a walka odbywa się w sposób turowy.

## Założenia konceptu

Program został napisany obiektowo w środowisku graficznym wykorzystując bibliotekę PyGame oraz Tk do rysowania okna. Każdy interaktywny obiekt gry, ze względu na brak wsparcia w domyślnej bibliotece, posiada własne funkcje rzucające eventy, które są obsługiwane w głównej pętli programu.

Program dodatkowo umożlwiwa wielokrotną grę podczas jednej sesji, a okna są odpowiednio ustawiane z pomocą zmiennych wybierającej obecny stan gry oraz menu.

## Inicjacja gry

Symulator przyjmuje pokemony obydwu graczy (od 1 do 6), a w przypadku gdy drugim graczem jest komputer wybiera on losowo z bazy danych pokemony w takiej samej ilości, co posiada pierwszy gracz.

Pokemony można dowolnie dodawać i usuwać z listy, a dodawanie pokemona odbywa sie na podstawie wyskakującego okienka blokującego okno główne, w którym możemy wybrać dowolnego z ponad 800 pokemonów z listy. Można ową listę również filtrować po nazwie oraz ID pokemona, aczkolwiek nie trzeba dodawać pełnej nazwy by wybranego pokemona wyszukać.

Gra może zostać zainicjowana dalej tylko w momencie, gdy liczba wybranych pokemonów pokrywa się z liczbą pokeballi.

## Walka

Walka odbywa się jak w oryginalnej serii - po kolei, w każdej rundzie trener desygnuje 1 pokemona do walki 1vs1. Walka odbywa się w sposób turowy.

Możliwy jest wybór 4 różnych akcji:

- Block - zwiększenie współczynnika obrony o 10% * 0.9^n, gdzie n to liczba, ile razy użyto bloku dla danego pokemona, zaczynając od 0. Ma to unimożliwić 'snowballowanie' w nieskończoność współczynnika obrony, zwłaszcza w przypadku potężniejszych pokemonów. Bot wykorzystuje ten ruch najczęściej gdy HP jego pokemona jest wysokie, a z czasem jak punkty życia pokemona spadają, częstotliwość występowania bloków zanika.
- Attack - atak przeciwnego pokemona atakiem normalnym. Wartość ta jestwyliczana na podstawie nieco zmodyfikowanego algorytmu z [Bulbapedii](https://bulbapedia.bulbagarden.net/wiki/Damage), bez wykorzystywania współczynników dla typów przeciwnego pokemona. Wartość obrażeń jest zawsze zaokrąglana w góre do wartości całkowitej. Jest to domyślny ruch bota.
- Special - atak wykorzystujący "typ" pokemona. Bierze on ze swojej listy typów jego rodzaj, a następnie bierze wartość ze słownika słabości pokemona przeciwnika, by wyliczyć mnożnik obarżeń. Typ specjalnego ataku pokemona można zawsze wybrać. Bot wkonuje ten ruch najczęściej przy wysokim mnożniku, jeśli mnoznik jest równy 0 to nigdy, a w przypadku 2 typów pokemona zawsze wybiera ten najlepszy.
- Change pokemon - podmiana pokemona na innego z drużyny Po śmierci walczącego pokemona, jeśli gracz posiada żyjące pokemony, należy wybrać nowego żyjącego pokemona do walki. Można również zachować pokemona i wyminić go na innego, zachowując jego statystyki. Bot nie może wycofać pokemona w trakcie gry, a po śmierci aktywnego zastępuje nieżyjącego pokemona losowym innym z żyjących.

Gra się kończy w momencie, gdy dany gracz nie posiada więcej żyjących pokemonów.

## Podsumowanie i samoocena
Pomimo, że na pewno nie jest to najlepsza gra z pokemonami w roli głównej (nie zaimplementowałem np.: zdjęć dla tych 800 pokemonów), uważam sam projekt za jak najbardziej udany, a efekt końcowy na oddanie projektu do oceny moim zdaniem sprawia przyjemność z korzystania, zwłaszcza po tak wielkiej włożonej w niego pracy. Być może w wolnym czasie będę ten projekt edytował poza zaliczeniem, wprowadzając np.: tabelkę umiejętności (której zalążek istnieł przez zdecydowaną większość projektu), animacje, czy wyskakujące okienka dialogowe.

Uwzględniając funkcjonalność programu, czytelność kodu oraz wykonaną dokumentacje i testy uważam, że projekt zasługuje na wysoką ocenę, na którą będąc szczerym liczę.
