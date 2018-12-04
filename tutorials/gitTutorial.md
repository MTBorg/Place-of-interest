# Git Tutorial (WIP)

#### Naming convention för branches
##### To be determined

### Instructions

För att klona repositoryn
```
git clone https://github.com/MTBorg/D0020E
```
Detta kommer att skapa en mapp som heter D0020E som är "up-to-date" med repon som ligger uppe på github.
Gå in i mappen
```
cd D0018E_Group1
```
Efter att ha klonat repon defaultas man till branchen master.
Du kan se vilken branch du är på genom att skriva (den som är markerad med * är den du är på)
```
git branch
```
Om du även vill se de branches som ligger på remoten lägger du till flaggan -a
```
git branch -a
```
(de branches som börjar med remotes/origin/ är de som ligger uppe på remoten och de övriga är de lokala på din maskin).
För att skapa en ny branch skriver du
```
git branch <branchName>
```

För att byta till en branch skriver du
```
git checkout <branchName>
```
alternativt för att skapa och komma direkt till den nya branchen
```
git checkout -b <branchName>
```
Med
```
git status
```
ser du alla filer du har ändrat på och med 
```
git diff
```
ser du de exakta ändringarna.
När du har gjort något du vill spara "committar" du det. För att markera vilka filer som ska commitas ("stageas") skriver du
```
git add <fileName>
```
eller för att stagea alla filer
```
git add -A
```
Sedan kan du commita ändringarna genom att skriva 
```
git commit -m <"This is a commit message">
```
Flaggan -m anger ett commit message och det är **VÄLDIGT** viktigt att du alltid skriver tydliga meddelanden.
För att unstagea en fil skriver du
```
git reset HEAD <fileName>
```
För att "pusha" dina commits till github repon skriver du
```
git push origin <branchName>
```
Du bör pusha varje gång du slutar arbeta.

Du kan ta bort en lokal branch (du kan inte vara på den branch du ska ta bort) genom
```
git branch -D <branchName>
```
Det kan hända att din lokala branch ligger efter motsvarande branch som ligger uppe på servern, du drar då ner ändringar med
```
git pull origin <branchName>
```
Du bör köra pull varje gång du har varit borta från projektet.

Det kan även hända att branches som ligger på github tas bort medans de ligger kvar på din maskin. För att uppdatera vilka branches som ligger på github skriver du
```
git remote update origin --prune
```

För att visa commit loggen för den branch du är på skriver du
```
git log
```
