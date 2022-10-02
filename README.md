# solveConflicts

### Link do aplikacji
https://solve-conflicts.herokuapp.com

---

Przedmiotem pracy jest aplikacja sieciowa Solve Conflicts służąca do nauki
o konfliktach w systemie kontroli wersji Git. Sprawne ich rozwiązywanie jest bardzo
przydatną umiejętnością dla każdego programisty, który pracuje w zespole. Solve
Conflicts zawiera osiem poziomów, które stopniowo wprowadzają coraz trudniejsze
problemy i sposoby ich rozwiązywania. W niniejszej pracy opisano użyte technologie,
sposób działania poszczególnych części aplikacji oraz trudności napotkane w trakcie
jej tworzenia.

The subject of the work is the Solve Conflicts web application used to learn about
conflicts in the Git version control system. Efficient Git conflict resolution is a very
useful skill for any programmer willing to work in a team. Solve Conflicts features
eight levels that gradually introduce more and more difficult problems and ways to
solve them. This paper describes used technologies, the mode of operation of indi-
vidual parts of the application and the difficulties encountered during it’s creation.

---

## Krótki opis

Głównym celem Solve Conflicts jest nauczenie osób początkujących (w Gicie)
w jaki sposób radzić sobie z konfliktami i jakie problemy mogą się z nimi wiązać.
Aplikacja składa się z ośmiu poziomów. Każdy z nich zaczyna się od poinformowania
użytkownika co musi zrobić, aby pomyślnie wykonać zadanie. Informacja przekazy-
wana jest za pomocą okienka (popup).

![image](https://user-images.githubusercontent.com/45509637/193462865-36a8e160-f7d0-4f9b-ab75-c25099d8b769.png)

Po zapoznaniu się z treścią zadania (która czasem ulega aktualizacji w trakcie
pracy) do dyspozycji użytkownika są następujące narzędzia:

### Interfejs drzewa katalogu

![image](https://user-images.githubusercontent.com/45509637/193462882-60b5a44f-1193-45d0-985c-09bae9537b89.png)

Ta część pokazuje dostępne dla użytkownika foldery i pliki, umożliwia ich roz-
wijanie i przełączanie się między nimi. Gdy za pomocą jakichś komend użytkownik
zmieni strukturę folderu, zostanie to zobrazowane w tej części aplikacji.

### Interaktywna konsola

![image](https://user-images.githubusercontent.com/45509637/193463015-a5453dd7-5daa-4a63-8064-2d7485ee5033.png)

Konsola umożliwia użytkownikowi wprowadzanie komend, które normalnie wy-
konywałby w powłoce systemowej. W naszej aplikacji będą to zazwyczaj komendy
Gitowe, ewentualnie niektóre polecenia modyfikujące pliki i foldery. W trosce o bez-
pieczeństwo aplikacji ograniczyliśmy możliwe komendy i ich wariacje. Mimo braku
całkowitej dowolności, możliwe do wykonania komendy są w pełni wystarczalne do
przejścia wszystkich poziomów. Po wpisaniu komendy użytkownik widzi odpowiedź
systemu na wpisaną komendę.

### Wizualizacja drzewa Gitowego

![image](https://user-images.githubusercontent.com/45509637/193463324-3d452128-38d4-468e-8874-f96378c492c2.png)


Wizualizacja przedstawia aktualny stan repozytorium użytkownika. Wszyst-
kie commity, merge, gałęzie oraz ich nazwy i odpowiednie wiadomości. Dodatkowo
wizualizacja na bieżąco jest aktualizowana gdy użytkownik wykona jakieś komendy
zmieniające stan repozytorium. Formalnie wizualizacja ma odwzorowywać to, co jest
wynikiem komendy 
`git log --graph --all --oneline --decorate --reflog.`

### Edytor tekstu

![image](https://user-images.githubusercontent.com/45509637/193463359-a6037d80-c440-486f-a925-3fa092ce8da7.png)

Edytor umożliwia edytowanie zawartości plików, między którymi użytkownik
może się przełączać za pomocą okna drzewa katalogu. Edytor umożliwia forma-
towanie składni dla wielu różnych języków. Po dopisaniu tekstu do pliku jest on
zapamiętywany po stronie frontendowej, ale żeby zapisać plik na stałe (backend)
użytkownik musi kliknąć przycisk: ’zapisz’.
