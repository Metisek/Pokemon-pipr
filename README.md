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

- Block - zwiększenie współczynnika obrony o 10% * 0.9^n, gdzie n to liczba, ile razy użyto bloku dla danego pokemona, zaczynając od 0. Ma to unimożliwić 'snowballowanie' w nieskończoność współczynnika obrony, zwłaszcza w przypadku potężniejszych pokemonów. Bot wykorzystuje ten najczęściej gdy HP jego pokemon a jest wysokie, a z czasem jak spada częstotliwość występowania bloków zanika.
- Attack - atak przeciwnego pokemona atakiem normalnym. Wartość ta jestwyliczana na podstawie nieco zmodyfikowanego algorytmu z [Bulbapedii](https://bulbapedia.bulbagarden.net/wiki/Damage), bez wykorzystywania współczynników dla typów przeciwnego pokemona. Wartość obrażeń jest zawsze zaokrąglana w góre do wartości całkowitej. Jest to domyślny ruch bota.
- Special - atak wykorzystujący "typ" pokemona. Bierze on ze swojej listy typów jego rodzaj, a następnie bierze wartość ze słownika słabości pokemona przeciwnika, by wyliczyć mnożnik obarżeń. Typ specjalnego ataku pokemona można zawsze wybrać. Bot wkonuje ten ruch najczęściej przy wysokim mnożniku, a jeśli jest równy 0 to nigdy, a w przypadku 2 typów zawsze wybiera ten najlepszy.
- Change pokemon - podmiana pokemona na innego z drużyny
Po kapitulacji jednego pokemona (jego hp spada do 0), na jego miejsce do walki wskakuje kolejny. Uwaga jeżeli pokemon zostanie wycofany, jego statystyki zostają zapisane (otrzymane obrażenia / zwiększona obrona). Program powinien umożliwiać grę dwóch użytkowników i grę przeciwko komputerowi który wykonuje logiczne ruchy.

Do obliczania obrażeń ataku pokemona można wykorzystać informacje z bulbapedii link. Należy wciąć pod uwagę typ ataku i odporność atakowanego pokemona na dany typ, oraz odpowiednie współczynnikii ataku i obrony.
## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab-stud.elka.pw.edu.pl/mbojarsk/pokemon.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab-stud.elka.pw.edu.pl/mbojarsk/pokemon/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

***

# Editing this README

When you're ready to make this README your own, just edit this file and use the handy template below (or feel free to structure it however you want - this is just a starting point!). Thank you to [makeareadme.com](https://www.makeareadme.com/) for this template.

## Suggestions for a good README
Every project is different, so consider which of these sections apply to yours. The sections used in the template are suggestions for most open source projects. Also keep in mind that while a README can be too long and detailed, too long is better than too short. If you think your README is too long, consider utilizing another form of documentation rather than cutting out information.

## Name
Choose a self-explaining name for your project.

## Description
Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

## Badges
On some READMEs, you may see small images that convey metadata, such as whether or not all the tests are passing for the project. You can use Shields to add some to your README. Many services also have instructions for adding a badge.

## Visuals
Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Installation
Within a particular ecosystem, there may be a common way of installing things, such as using Yarn, NuGet, or Homebrew. However, consider the possibility that whoever is reading your README is a novice and would like more guidance. Listing specific steps helps remove ambiguity and gets people to using your project as quickly as possible. If it only runs in a specific context like a particular programming language version or operating system or has dependencies that have to be installed manually, also add a Requirements subsection.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
