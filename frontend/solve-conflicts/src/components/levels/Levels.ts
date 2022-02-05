export const levels = [
  [
    {
      message: `Witaj w solveConflicts! Mamy nadzieję, że
      wspólnie nauczymy się czegoś ciekawego o rozwiązywaniu
      konfliktów w systemie kontroli wersji GIT.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Razem ze swoim kolegą planujecie umieścić na swojej stronie
      internetowej przepis na naleśniki. W tym celu każdy z Was
      napisał własną wersję tego jakich proporcji należy użyć do ciasta.
      Musisz teraz zadecydować, który przepis jest lepszy i zostanie opublikowany.
      Rozpocznij od wpisania komendy: ‘git branch‘.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Zauważ, że znajdujesz się aktualnie na gałęzi ‘master’, gdzie
      jest plik z Twoją wersją przepisu. Twój kolega ma przepis na osobnej
      gałęzi (friend branch). Spróbuj automatycznie połączyć te dwie
      gałęzie przy użyciu komendy: git merge friend_branch”
      W razie potrzeby pamiętaj o komendach: ‘help’ oraz ‘hint’.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Niestety… zawartości plików są istotnie różne i GIT nie jest
      w stanie ich automatycznie połączyć. Zauważ, że zawartość pliku
      ‘przepis.txt’ uległa zmianie. Znajdują się w nim miejsce z dwoma wyraźnie
      oddzielonymi sekcjami. Sekcja HEAD oznacza wersję Twojej gałęzi. Druga
      sekcja to zmiany kolegi. Twoim zadaniem jest zmodyfikować ten plik wybierając
      jedną z dwóch wersji, po czym użyć komendy ‘git add’ a następnie dokończyć merge.`,
      width: "600px",
      height: "300px",
      stage: 2,
    },
  ],
  [
    {
      message: `Pierwszy poziom był dość prosty. Teraz będzie nieco trudniej.
      Masz za zadanie połączyć dwie wersje pliku ‘style.json’ z konfiguracją
      stylowania Waszej strony internetowej. W tym pliku są trzy sekcje (“header”,
      “main-table” oraz “footer”). Rozpocznij przejrzenia zawartości pliku oraz
      próby zmergowania tych gałęzi!`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `O ile obie wersje pliku mają taką samą wersję
      sekcji “main-table”, to pozostałe sekcje się od siebie różnią. Wspólnie
      z kolegą ustaliliście, aby zachować Twoją wersję kawałka odpowiadającego
      za sekcję “footer”, ale wersję kolegi jeżeli chodzi o “header”.
      Do dzieła!`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
  ],
  [
    {
      message: `Całkiem nieźle! Udało Ci się rozwiązać już dwa konflikty. Ale czy
      konflikt może wystąpić jedynie przy próbie wykonania ‘git merge’? Okazuje
      się, że konflikty mogą pojawiać się również przy innych komendach
      zmieniających strukturę repozytorium.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Jedną z nich jest git rebase. Pomoże nam ono uporządkować historię
      naszego repozytorium. Pracowałeś ostatnio nad dwiema gałęźmi, z których jedna
      wyliczała liczby Catalana, a na drugiej umieściłeś kod szeregu Taylora.
      Postanowiłeś, że możesz połączyć
      ten plik w jeden i sprawić żeby historia wyglądała tak, jakbyś nigdy nie rozdzielał pracy na dwoje.
      Spróbuj wykonać komendę ‘git rebase liczby_catalana’.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Funkcja silnia posiada dwie różne implementacje. Wybierz tę, z której wolałbyś korzystać, a następnie ‘pogódź’ resztę pliku zachowując ukończone
      implementacje pozostałych dwóch funkcji. Po wszystkim użyj komendy ‘git rebase’ z flagą ‘–continue’.`,
      width: "600px",
      height: "300px",
      stage: 2,
    },
  ],
  [
    {
      message: `Razem z kilkoma znajomymi postanowiliście wystąpić w drużynowym konkursie
      programistycznym. Polega on na tym, że każdy próbuje wymyślić swoją
      strategię na rozwiązanie problemu optymalizacyjnego, a po jakimś czasie
      i naradach drużyna przechodzi w tryb implementacji kodu.`,
      width: `600px`,
      height: `300px`,
      stage: 1,
    },
    {
      message: `Wpadłeś na bardzo skomplikowany, ale obiecujący pomysł. Niestety
      wymyślenie go zabrało Ci trochę czasu. Chcesz go nadrobić. Pomyślałeś
      więc, że skorzystasz z szablonu kodu, który w międzyczasie zdążył już
      napisać jeden z Twoich kolegów. Wykonał on już kilka komitów na gałęzi
      swojego kodu, ale dla Ciebie
      istotny jest tylko jeden z nich o nazwie “defines”. W tym komicie jest
      kilka przydatnych linii kodu, których nie ma sensu przepisywać
      automatycznie.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Za pomocą “git cherry-pick COMMIT” wyłuskaj komit, którego
      potrzebujesz i dołącz go do swojej gałęzi, a jeżeli w międzyczasie pojawi
      się również jakiś konflikt, to go rozwiąż!`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `A niech to! Znowu jeden z tych przeklętych konfliktów! Na pewno dasz sobie z nim radę.`,
      width: "600px",
      height: "300px",
      stage: 2,
    },
    {
      message: `Może wydawać się to dziwne, ale jedna z sekcji powstałych w pliku
      konfliktowym jest pusta, ale oznacza, że git oznacza brak zmian, jako zmianę.`,
      width: "600px",
      height: "300px",
      stage: 2,
    },
  ],
  [
    {
      message: `Ten poziom, będzie krótką odskocznią od rozwiązywania konfliktów, ale
      też niesie w sobie nieco przydatnej wiedzy. Wyobraź sobie sytuację, gdzie
      w pracy dostałeś zlecenie na wykonanie połączenie dwóch (lub więcej)
      bardzo rozbudowanych gałęzi. Rozwiązałeś już część konfliktów, ale
      w trakcie pracy, Twój szef powiedział, żeby się jednak wstrzymać
      z mergowaniem, bo nie jest jeszcze do końca pewien, które wersje plików
      chciałby zostawić.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Jedzie na urlop i wróci dopiero za tydzień, więc nie ma co
      bezczynnie czekać. W tej sytuacji należy zrezygnować z aktualnego stanu
      i próbować wrócić do prac na jednej z gałęzi. Jak to zrobić? Okazuje się,
      że sprawa jest bardzo prosta. Wystarczy wykonać komendę “git merge --abort”,
      aby repozytorium powróciło do stanu sprzed wywołania komendy merge.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Okazuje się, że flaga --abort działa
      w bardzo podobny sposób, jeżeli chcielibyśmy cofnąć zmiany w trakcie
      ‘git rebase’ albo ‘git cherry-pick’`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
  ],
  [
    {
      message: `Razem z bratem planujecie wyjechać latem w góry pozdobywać Tatrzańskie
      szczyty. W tym celu postanowiliście zrobić kalendarz wypraw na szlaki.
      Każdy z Was podał jakieś propozycje tras, i teraz pora na połączenie
      pomysłów. Użyj komendy git merge!`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Niestety okazuje się, że merge się nawet nie rozpoczął… bo z pliku
      ‘wyjazd.txt’ znalazła się jakaś przypadkowa zmiana od ostatniego komita.
      W takiej sytuacji najlepiej byłoby pozbyć się tych niepotrzebnych zmian
      i wrócić do sytuacji bezpośrednio po zrobieniu ostatniego komita. Na
      szczęście Git daje nam taką możliwość! Z pomocą przychodzi komenda git restore.`,
      width: "600px",
      height: "300px",
      stage: 2,
    },
    {
      message: `Użyj tej komendy by, przywrócić prawidłowy stan dla pliku wyjazd.txt,
      a następnie połącza gałęzie ‘pat’ i ‘mat’ (jeżeli zajdzie konflikt, to
      zadbaj o jego rozwiązanie)`,
      width: "600px",
      height: "300px",
      stage: 2,
    },
  ],
  [
    {
      message: `Postanowiłeś zrobić swoim rodzicom prezent! Na ich trzydziestą rocznicę
      ślubu chcesz zrobić im remont mieszkania. Nic prostszego… Już nawet
      przygotowałeś arkusz, w którym wpisałeś co chcesz im wyremontować.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Jak to jednak w życiu bywa… rodzice po tym jak usłyszeli, że chcesz
      zrobić im prezent, postanowili wprowadzić pewne poprawki do arkusza…
      Stworzyli nawet nową gałąź w systemie GIT by tam notować swoje zmiany.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Poprosili Cię o uwzględnienie tych zmian… Sytuacja jest opłakana, ilość
      poprawek, które wprowadzili rodzice jest zatrważająca. Trudno Ci będzie w
      takiej sytuacji odmówić. Nie wiemy jak uratować Twój portfel, ale możemy
      pokazać Ci metodę na zaoszczędzenie czasu.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `Dla komendy merge można podać flagę ‘-X’, która pozwala na określenie
      strategii przy merdżowaniu. i tak gdy podamy ‘-X ours’ to wszystkie
      konflikty będą rozstrzygane na korzyść HEAD, a dla ‘-X theirs’ na korzyść drugiej gałęzi.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `W tym poziomie, możesz albo spróbować wykonać wszystkie zmiany ręcznie
      (zawsze zostawiając wersje z gałęzi rodziców), albo po prostu skorzystać z flagi -X`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
  ],
  [
    {
      message: `Prowadzisz prace nad projektem programistycznym na gałęzi ‘develop’.
      Na potrzeby naprawy kawałka kodu stworzyłeś gałąź bugFix i dokonałeś
      na niej kilka zmian. Twoim zadaniem jest podłączenie tych zmian
      do głównego nurtu gałęzi. Możesz to zrobić za pomocą ‘merge’, albo ‘rebase’.`,
      width: "600px",
      height: "300px",
      stage: 1,
    },
    {
      message: `
      A jednak postał konflikt. Rozwiąż go i odbierz swój wymarzony dyplom ukończenia kursu!.`,
      width: "600px",
      height: "300px",
      stage: 2,
    },
  ],
];
