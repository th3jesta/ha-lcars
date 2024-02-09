**Haftungsausschluss: Diese Readme-Datei wurde automatisch von ChatGPT übersetzt. Wir übernehmen keine Verantwortung für mögliche Ungenauigkeiten oder Fehler in der Übersetzung. Bitte beachten Sie, dass dies eine automatisierte Übersetzung ist.**

**(Übersetzung gültig ab Version 2.2.2 des Themes.)**

# Home Assistant LCARS
Star Trek LCARS theme für Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration) 

<a href="https://discord.gg/gGxud6Y6WJ"><img src="https://discordapp.com/api/guilds/1059179538371858493/widget.png?style=banner2" width="140px" alt="Discord Banner 2"/></a>

Farbcodes und Schriftauswahl von https://www.thelcars.com
    --Danke Jim Robertus!

## Beispiele
### Dashboard
![image](https://user-images.githubusercontent.com/38670315/212081440-039e5481-ca2b-4c08-814c-2a83d6a5a377.png "Automatisierungen für heißen Earl Grey Tee nicht inbegriffen.")

### Bearbeitungsmodi
![image](https://user-images.githubusercontent.com/38670315/212082080-d3543d1a-9cb2-4205-93cf-4e10829db8f8.png)

### Mobile Ansicht
<img src="https://user-images.githubusercontent.com/38670315/212080834-70b1554e-602a-42a6-8bf8-b42bf99463d5.png" width="360" /> <img src="https://user-images.githubusercontent.com/38670315/212081003-790ced32-f14d-47dc-9f13-cd711c5f02aa.png" width="360" />

### Enthaltene Themes
![LCARS Themes](https://user-images.githubusercontent.com/38670315/210556056-26458f3d-60e4-400f-89df-f0b8cc68a6a2.png)
Classic, Lower Decks, Romulus, Cardassia, Kronos, Nemesis.
    
## Präambel
Ich bin definitiv kein echter Webentwickler und habe mich mit Hilfe von Stack Exchange und verschiedenen Blogs zu CSS-Techniken in die erste Veröffentlichung hineingestolpert. Mein Hauptziel war und ist es immer noch, dieses Theme zu 100% auf CSS/JS-Basis zu halten, ohne zusätzliche Ressourcen außer der Schriftart zu benötigen. Ich bin sicher, es gibt bessere Möglichkeiten, alles, was ich bisher gemacht habe, umzusetzen. Daher sind Pull Requests willkommen. Ich werde Dinge weiter verbessern, während ich lerne, und mehr Kommentare zu meinem CSS hinzufügen, damit Sie wissen können, was Dinge tun und mir vielleicht sagen können, wie es besser sein könnte, wenn Sie es wissen. Ich habe dieses Theme mit den meisten der mit Home Assistant ausgelieferten Standardkarten und einigen in HACS verfügbaren Karten wie der Mail and Packages-Karte getestet. Es könnten jedoch noch einige Karten katastrophal kaputt sein. Erstellen Sie einfach ein Problem und ich werde mich darum kümmern.

## Installationsanweisungen
### Voraussetzungen
#### I. Themes aktivieren und card-mod installieren

1. Installieren Sie `card-mod` gemäß den Anweisungen auf seiner [GitHub-Seite](https://github.com/thomasloven/lovelace-card-mod "card-mod").

2. Stellen Sie sicher, dass Sie in Ihrer **configuration.yaml**-Datei Folgendes haben:
```yaml
frontend:
  javascript_version: latest
  themes: !include_dir_merge_named themes
  extra_module_url:
    - /local/community/lovelace-card-mod/card-mod.js #or wherever you ended up putting card-mod.js
```
3. Unter dem Home Assistant **Config**-Ordner erstellen Sie einen neuen Ordner mit dem Namen **themes**.
4. **Starten** Sie Home Assistant neu, um die Änderungen zu übernehmen.

#### II. Schriftart und JavaScript-Datei hinzufügen

Für dieses Theme müssen Sie sowohl die Schriftart `Antonio` als auch die Datei `lcars.js` als Ressourcen zu Ihrer Lovelace-Konfiguration hinzufügen.

Navigieren Sie zu `Einstellungen` → `Dashboards` → `Drei-Punkt-Menü` → `Ressourcen` und fügen Sie die folgenden neuen Ressourcen hinzu:
1. `https://fonts.googleapis.com/css2?family=Antonio:wght@400;700&display=swap` und wählen Sie 'stylesheet'
2. `https://cdn.jsdelivr.net/gh/th3jesta/ha-lcars@js-main/lcars.js` und wählen Sie JavaScript

##### -ODER-
Wenn Sie dem zufälligen JavaScript von jemand anderem, das auf einem CDN gehostet wird, nicht vertrauen (ich verstehe das), können Sie die `lcars.js`-Datei direkt von GitHub herunterladen, selbst überprüfen und sie in Ihrem `<home-assistant-Verzeichnis>/www/community/` ablegen; **dies muss bei jedem HA-LCARS-Update erfolgen.**
**Fügen Sie `/local/community/lcars.js` nicht zu `extra_module_url` hinzu; es wird dort nicht funktionieren.**

**WENN SIE CLOUDFLARE VOR IHRER WEBSITE VERWENDEN:**
Löschen Sie Ihren Website-Cache in CloudFlare (Cache löschen unter Schnellaktionen) immer dann, wenn Sie die lokale Datei aktualisieren oder wenn Sie den JSDelivr-Link verwenden und eine neue Version von HA-LCARS veröffentlicht wird. Dies muss geschehen, unabhängig davon, ob Sie den JSDelivr-Link verwenden oder ihn in Ihren www-Ordner legen. Es sei denn, Sie teilen es ihm mit, CloudFlare puffert alles in Ihrer Website, was es kann.

#### III. Uhr einrichten
Damit die Uhr funktioniert, müssen Sie die Integration für Zeit & Datum einrichten, indem Sie folgendes zu Ihrer configuration.yaml hinzufügen:
```yaml
sensor:
  - platform: time_date
    display_options:
      - 'time'
      - 'date'
      - 'date_time'
      - 'date_time_utc'
      - 'date_time_iso'
      - 'time_date'
      - 'time_utc'
```

Weitere Informationen:
https://www.home-assistant.io/integrations/time_date/

#### IV. Entitäten erstellen
Dieses Theme verfügt über zwei Steuerelemente für Ton und Texturen, für die einfache Umschalt-Entitäten erstellt werden müssen. Erstellen Sie sie, indem Sie zu Einstellungen > Geräte & Dienste > Helfer gehen und zwei vom Typ **Umschalten** mit folgenden Namen erstellen:
- LCARS-Sound (Entitäts-ID sollte `input_boolean.lcars_sound` sein)
- LCARS-Textur (Entitäts-ID sollte `input_boolean.lcars_texture` sein)
<img width="644" alt="image" src="https://user-images.githubusercontent.com/38670315/234965572-defd6f0e-8af3-4e16-9cb2-408d665d531a.png">

Diese Entitäten können direkt durch Anzeigen der Entität gesteuert werden, oder Sie können sogar Schaltflächen zu Ihrem Dashboard hinzufügen, um sie zu steuern, genauso wie jede andere Entität.

### Theme installieren
Installieren Sie es über HACS, indem Sie nach "LCARS" suchen, oder laden Sie die [neueste Version](https://github.com/th3jesta/ha-lcars/releases/latest) herunter, entpacken Sie sie und legen Sie den Ordner "lcars" in Ihren Ordner "themes".

### Theme aktivieren
#### Option 1: Über das Profil
1. Öffnen Sie Ihr Home Assistant **Profil**
2. Wählen Sie unter **Themes** eines der neuen LCARS-Themes aus
3. Rufen Sie den Dienst `frontend.reload_themes` auf.

#### Option 2: Festlegen des Standard-Backends-Themas
Damit dieses Theme automatisch als Standard für das Backend ausgewählt wird, fügen Sie die folgende Automatisierung zu Ihrem Home Assistant hinzu:
```yaml
- alias: Set Default Theme
  description: ''
  trigger:
  - event: start
    platform: homeassistant
  condition: []
  action:
  - data:
      name: LCARS Default # or whichever other theme is available, like LCARS Lower Decks
    service: frontend.set_theme
```
## Anleitung zur Verwendung
### Klassen
Das Theme enthält einige Klassen, die Karten hinzugefügt werden können, um ihnen spezielles Styling zu verleihen:
```yaml
card_mod:
  class: header
```
_Die Klassennamen sind nur Hinweise darauf, für welche Arten von Karten sie gedacht waren, aber die Klassen können auf jede gewünschte Karte angewendet werden. Ich kann jedoch nicht garantieren, wie gut sie außerhalb ihrer beabsichtigten Verwendungszwecke funktionieren werden._

Die Klassen sind wie folgt:
1. `header` `header-right` `header-contained` `header-open` - obere blaue Leiste (im Standard-Theme) für Markdown-Karten mit einer `H1`-Zeile, die einen Abschnitt startet
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>
    
```yaml
type: markdown
card_mod:
  class: header
content: '# header'

type: markdown
card_mod:
  class: header-right
content: '# header-right'

type: markdown
card_mod:
  class: header-contained
content: '# header-contained'

type: markdown
card_mod:
  class: header-open
content: '# header-open'
```

</td>
<td>
<img width="316" alt="image" src="https://user-images.githubusercontent.com/38670315/212480715-ca72d5e5-1950-4f75-9b14-8b67fcebdcd0.png">
</td>
</tr>
</table>

2. `middle` `middle-right` `middle-contained` - seitliche rote Leiste (im Standard-Theme) für Nicht-Schaltflächen-Abschnitte unterhalb des `header` und oberhalb des `footer`
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
type: markdown
card_mod:
  class: middle
content: '# middle'

type: markdown
card_mod:
  class: middle-right
content: '# middle-right'

type: markdown
card_mod:
  class: middle-contained
content: '# middle-contained'
    
type: markdown
card_mod:
  class: middle-blank
content: '# middle-blank'
```

</td>
<td>
<img width="316" alt="image" src="https://user-images.githubusercontent.com/38670315/234729314-6bd0371e-5839-4b6e-8996-bb5ce417824f.png">
</td>
</tr>
</table>

3. `footer` `footer-right` `footer-contained` `footer-open` - untere graue Leiste (im Standard-Theme) für die letzte Karte in einem Abschnitt
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
type: markdown
card_mod:
  class: footer
content: '# footer'

type: markdown
card_mod:
  class: footer-right
content: '# footer-right'

type: markdown
card_mod:
  class: footer-contained
content: '# footer-contained'

type: markdown
card_mod:
  class: footer-open
content: '# footer-open'
```

</td>
<td>
<img width="314" alt="image" src="https://user-images.githubusercontent.com/38670315/212480789-62e37686-dd35-4a49-a3e7-1d974b7eb133.png">
</td>
</tr>
</table>

4. `button-small` - quadratische Schaltflächen, die für mittlere Abschnitte sowie horizontale Stapel und Raster vorgesehen sind
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
type: light
entity: light.jesse_s_desk
name: Desk Lamp
card_mod:
  class: button-small
```

</td>
<td>
<img width="107" alt="image" src="https://user-images.githubusercontent.com/38670315/210178400-5d39e821-328f-4bd5-907d-1863dc2f7ff6.png">
</td>
</tr>
</table>

5. `button-large` - abgerundete Schaltfläche, die eigenständig außerhalb der Abschnitte `header`/`middle`/`footer` stehen soll
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
show_name: true
show_icon: true
type: button
tap_action:
  action: call-service
  service: frontend.reload_themes
  data: {}
  target: {}
show_state: true
card_mod:
  class: button-large
```

</td>
<td>
<img width="318" alt="image" src="https://user-images.githubusercontent.com/38670315/210178438-59da5bce-4f86-4de6-94e3-830aa845293e.png">
</td>
</tr>
</table>

6. `button-lozenge` `button-lozenge-right` - pilleförmige Schaltfläche; funktioniert nur auf Standard-Schaltflächenkarten; funktioniert auch auf Schaltflächenkarten in horizontalen Stapeln und Rastern bis zu zwei Spalten Breite; mehr Spalten werden unzuverlässig und sind nicht ratsam
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
show_name: true
show_icon: true
type: button
tap_action:
  action: toggle
entity: switch.speakers
icon: mdi:speaker-multiple
card_mod:
  class: button-lozenge
  
show_name: true
show_icon: true
type: button
tap_action:
  action: toggle
entity: switch.lightsaber
card_mod:
  class: button-lozenge-right
```

</td>
<td>
<img width="159" alt="image" src="https://user-images.githubusercontent.com/38670315/212760869-5a09e9c0-9d61-4b48-af3c-5040a82c1722.png">
</td>
</tr>
</table>

7. `button-bullet` `button-bullet-right` - ähnlich wie das Lozenge, aber mit einer abgerundeten Seite; gleiche Spaltenbeschränkungen gelten
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
show_name: true
show_icon: true
type: button
tap_action:
  action: toggle
entity: light.bedroom_tree
card_mod:
  class: button-bullet
  
show_name: true
show_icon: true
type: button
tap_action:
  action: toggle
entity: switch.counter_lights
card_mod:
  class: button-bullet-right
```

</td>
<td>
<img width="158" alt="image" src="https://user-images.githubusercontent.com/38670315/212761051-a9cb1cc8-b445-46d5-9270-171249f6d63f.png">
</td>
</tr>
</table>

8. `button-capped` `button-capped-right` - ähnlich wie das Bullet, aber auf der runden Seite abgeschlossen; gleiche Spaltenbeschränkungen gelten
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
show_name: true
show_icon: true
type: button
tap_action:
  action: toggle
entity: light.bathroom
card_mod:
  class: button-capped
  
show_name: true
show_icon: true
type: button
tap_action:
  action: toggle
entity: switch.built_in
card_mod:
  class: button-capped-right
```

</td>
<td>
<img width="164" alt="image" src="https://user-images.githubusercontent.com/38670315/213804819-a9949ad2-4b9c-4539-ae5a-075dec098b11.png">
</td>
</tr>
</table>

9. `bar` `bar-right` `bar-large` `bar-large-right` - eigenständige Kopfzeilentyp-Leiste; nur für und mit Markdown-Karten beabsichtigt und getestet
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
type: markdown
content: '# bar'
card_mod:
  class: bar
  
type: markdown
content: '# bar-large'
card_mod:
  class: bar-large
  
type: markdown
content: '# bar-right'
card_mod:
  class: bar-right
  
type: markdown
content: '# bar-large-right'
card_mod:
  class: bar-large-right
```

</td>
<td>
<img width="313" alt="image" src="https://user-images.githubusercontent.com/38670315/212764544-04adc98c-8146-4f9b-9eef-7696689dce4c.png">
</td>
</tr>
</table>

### Erstellen eigener Farbthemen
Benutzerdefinierte Themen können unten in `lcars.yaml` erstellt werden. Oder suchen Sie nach "===THEMES", das bringt Sie direkt dorthin. Um Ihr eigenes Thema zu erstellen, kopieren Sie den Abschnitt "LCARS Default" ans Ende der Datei und ändern Sie die `lcars-ui-*`- und `lcars-card-*`-Variablen nach Belieben, unter Verwendung der Farbverweise oben in der Datei, [Die LCARS-Website](https://www.thelcars.com/colors.php) oder definieren Sie Ihre eigenen.

## Tipps und Tricks
_Wenn Sie hier etwas hinzufügen möchten, erstellen Sie eine Pull-Anfrage mit Ihrem Tipp, und ich werde sie überprüfen und zur Liste hinzufügen._
* Nutzen Sie Vertical Stack-Karten. Egal, ob in diesem Theme oder einem anderen Theme, sie sind unschätzbar, um Dashboards organisiert zu halten. In LCARS sollte eine Vertical Stack-Karte zuerst eine Markdown-Karte mit dem Titel der Gruppe und der Klasse `header` enthalten, dann beliebig viele Karten mit der Klasse `middle` und einzelne Schaltflächen oder horizontale Stapel oder Raster mit der Klasse `button`, und schließlich sollte die Klasse `footer` auf der letzten Karte im Vertical Stack angewendet werden. Sie können diese Formation in allen Screenshots oben auf dieser Seite sehen. Hier ist ein Beispiel für eine Vertical Stack-Karte und deren Inhalt:
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
type: vertical-stack
cards:
  - type: markdown
    card_mod:
      class: header
    content: '# Climate'
  - type: weather-forecast
    entity: weather.home
    card_mod:
      class: middle
  - type: thermostat
    entity: climate.dining_room
    card_mod:
      class: footer
```

</td>
<td>
<img width="308" alt="image" src="https://user-images.githubusercontent.com/38670315/210189965-b73662a8-5390-46ea-9450-b0043e6d2547.png">
</td>
</tr>
</table>

* Sie können eine leere Kopf- oder Fußzeile erstellen, indem Sie eine Markdown-Karte erstellen und `## &nbsp;` in das Feld für den Inhalt setzen, und die Größe ändern, indem Sie die Anzahl der `#` ändern. Es sieht so aus:
![image](https://user-images.githubusercontent.com/38670315/210792537-f25c74.0d-1ad3-4ac7-8a31-59ad04cf38fb.png)

* Wenn Sie das Theme nur auf ein Dashboard oder eine Karte anwenden, wird die Schriftart auf den Karten nicht gerendert. Sie können die Schriftart gewaltsam auf einer pro-Karten-Basis laden, indem Sie dem folgenden Stil zu jeder Karte hinzufügen:
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
type: markdown
content: '# Card-level theming'
theme: LCARS Default
card_mod:
  class: header
  style: |
    ha-card > * {
      font-family: Antonio
    }
```

</td>
<td>
<img width="308" alt="image" src="https://user-images.githubusercontent.com/38670315/236198970-0c06be57-d331-41d8-b692-95741b68bf5e.png">
</td>
</tr>
</table>

* Wenn Sie die Schriftart selbst hosten möchten, z. B. wenn Sie eine Home Assistant-Instanz in einem Auto oder in einem abgeschotteten Netzwerk ausführen, können Sie lernen, wie Sie die Schriftart herunterladen und von der Issue https://github.com/th3jesta/ha-lcars/issues/69 installieren.

* Sie können die Ausrichtung von Text in einer Karte, wie zum Beispiel der Markdown-Karte für `header-right`, ändern, indem Sie benutzerdefiniertes CSS pro Karte hinzufügen, wie folgt:
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
card_mod:
  class: header-right
  style: |
    ha-card {
      text-align: right;
    }
```

</td>
<td>
<img width="308" alt="image" src="https://github.com/th3jesta/ha-lcars/assets/38670315/41c38e14-5041-4355-8581-07c82c96ceca">
</td>
</tr>
</table>

* Sie können die Hintergrundfarbe einer Schaltfläche auf die Farbe des Lichts setzen, indem Sie benutzerdefiniertes CSS pro Karte hinzufügen, wie folgt:
<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>

```yaml
card_mod:
  class: button-capped-right
  style: |
    ha-card {
      {% if is_state('light.terasa', 'on') %}
        {% set rgb_color = state_attr('light.terasa', 'rgb_color') %}
        background-color: rgba({{ rgb_color[0] }}, {{ rgb_color[1] }}, {{ rgb_color[2] }}, 1);
        color: black;  /* or any other logic for text color */
      {% else %}
        background-color: #dd4444;
        color: black;
      {% endif %}
    }
```

</td>
<td>
<img width="308" alt="image" src="https://github.com/th3jesta/ha-lcars/assets/38670315/8417b463-0d0b-447d-8a7b-374d47f1e251">
</td>
</tr>
</table>

## Bekannte Probleme
* Schriftart- und Seitenleisten- sowie Kopfzeilen-CSS-Stile werden nur geladen, wenn zuerst ein Dashboard geladen wurde. Wenn Sie direkt zu einer Nicht-Dashboard-Seite navigieren, ohne zuerst ein Dashboard zu laden, wird es ziemlich schrecklich aussehen, aber trotzdem funktional sein. Laden Sie einfach ein Dashboard und klicken Sie auf die Zurück-Schaltfläche. Dies ist eine Eigenart des [card-mod](https://github.com/thomasloven/lovelace-card-mod)-Addons, auf dem dieses Theme basiert, sodass ich es nicht reparieren kann.
* card-mod-Klassen funktionieren nicht mit Vertical Stack- und Horizontal Stack-Karten (obwohl sie mit den enthaltenen Karten funktionieren). Dies ist eine Eigenart des [card-mod](https://github.com/thomasloven/lovelace-card-mod)-Addons, auf dem dieses Theme basiert, sodass ich es nicht reparieren kann. Es gibt jedoch einen Workaround, den ich identifiziert habe, aber mich entschieden habe, ihn derzeit nicht einzuschließen. Bitte reichen Sie eine Feature-Anfrage ein, wenn Sie möchten, dass dies aufgenommen wird.
* ~~Das Zusammenklappen und Ausklappen der Seitenleiste oder das Zoomen der Oberfläche wird mit den Überlagerungen von Rauschen und Gradienten stören. Ein einfacher Refresh setzt alles wieder richtig. Ich hoffe, eine Möglichkeit zu finden, die Pseudo-Elemente, die die Texturen enthalten, dynamisch an den DOM anzupassen. PRs sind willkommen. [Fehler hier](https://github.com/th3jesta/ha-lcars/issues/4).~~
* Menüseiten wie Entwicklungswerkzeuge und Profil sind funktionsfähig, aber nicht optimal. Leider kann ich nicht viel dagegen tun, da card-mod keine Methode zum Ändern dieser Seiten bietet. Fehlermeldungen für alles, was komplett kaputt und unbrauchbar ist, das ich übersehen haben könnte, sind willkommen, ebenso wie PRs, um die Dinge zu verbessern.
* Manchmal werden beim Laden eines Dashboards nicht alle CSS-Stile geladen, und alle oder die meisten Karten sehen aus wie die `button-large`-Karten. Dies tritt häufiger bei großen Dashboards auf. Versuchen Sie, die Seite neu zu laden, und wenn das nicht funktioniert, laden Sie ein kleineres Dashboard und kehren Sie dann zum problematischen Dashboard zurück.

## Dank
- Vielen Dank an @JHuckins für die Unterstützung bei der Farbgestaltung und das Testen!
- Vielen Dank an @csanner für die neuen Klassen und zusätzlichen Fixes und Tweaks!
- Vielen Dank an @Anthrazz für die Bar-Klassen!
- Vielen Dank an @mtezzo für die Schalter-Entität für Texturen/Gradienten und das Modern-Theme (mein neues Lieblings-Theme)!
- Vielen Dank an @CmdreIsaacHull für verschiedene Fixes, Verbesserungen, Themen und neue Klassen!
- Vielen Dank an @askpatrickw für die Lösung, wie die Schriftart selbst gehostet werden kann!
- Vielen Dank an @z3r0l1nk für den Trick mit den farblich abgestimmten Lichtschaltflächen!
- Vielen Dank an @smugleafdev für den Tipp mit dem rechtsbündigen Text!
- Vielen Dank an @Routhinator (über Discord) für die Fixierung des rechten Fußzeilenproblems!

## Links
**Discord:** https://discord.gg/gGxud6Y6WJ

**LCARS-Ressourcen:** https://www.thelcars.com
