**Haftungsausschluss: Diese Readme-Datei wurde automatisch von ChatGPT-5mini übersetzt. Wir übernehmen keine Verantwortung für mögliche Ungenauigkeiten oder Fehler in der Übersetzung. Bitte beachten Sie, dass dies eine automatisierte Übersetzung ist.**

**(Übersetzung gültig ab Version 4.0.0 des Themes.)**
# Home Assistant LCARS
Star Trek LCARS-Theme für Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration) 

<a href="https://discord.gg/gGxud6Y6WJ"><img src="https://discordapp.com/api/guilds/1059179538371858493/widget.png?style=banner2" width="140px" alt="Discord Banner 2"/></a>

Farb-Codes und Schriftart-Auswahl von https://www.thelcars.com  
    --Danke Jim Robertus!

# 💥BREAKING CHANGES IN 4.0💥
1. Home Assistant LCARS basiert auf der Funktionalität von [card-mod](https://github.com/thomasloven/lovelace-card-mod "card-mod"). Version 4.x von card-mod enthält zahlreiche inkompatible Änderungen für alle Themes, einschließlich Home Assistant LCARS. Die meisten Standardkarten, die dieses Theme verwenden, sollten sich ohne Probleme aktualisieren. Karten mit benutzerdefiniertem CSS, das über ``card-mod: style:`` angewendet wurde, müssen möglicherweise manuell auf die neuen Element-Selektoren von card-mod aktualisiert werden (z. B. ``hui-card`` statt ``ha-card``). Siehe die [README](https://github.com/thomasloven/lovelace-card-mod/blob/master/README.md) und [README-application](https://github.com/thomasloven/lovelace-card-mod/blob/master/README-application.md) von card-mod als Einstieg.
2. Aufgrund der oben genannten Änderungen werden einige Karten nicht mehr unterstützt oder benötigen spezielle Workarounds. Der Workaround besteht darin, die Karte in einen vertikalen oder horizontalen Stack zu legen. Dadurch ändert sich, wie card-mod die Karte erkennt und das Theme anwendet. Bekannte problematische Karten:
   - ⚠️ custom-button-card: Stack-Workaround für einige Theme-Klassen erforderlich. Wenden Sie die gewünschte Theme-Klasse auf den Stack an. Verwenden Sie die Stiloptionen der Custom Button Card, um das gewünschte Aussehen zu erzielen.
3. Balkenkarten können nun skaliert werden, indem die Schriftgröße der Karte geändert wird (siehe [Tipps und Tricks](#custom-bar-sizes) unten). Daher darf das Markdown **keine** Schriftgrößen enthalten, z. B. die Überschrift ``#``.
4. Dies ist nahezu eine vollständige Neufassung, einschließlich mehrerer CSS-Optimierungen. Dashboards, die mit früheren Versionen erstellt wurden, müssen möglicherweise aufgrund kleiner Änderungen bei Abständen und Innenabständen leicht angepasst werden.

# 🎉NEUE FEATURES IN 4.0🎉
### Themed Stacks
Vertikale und horizontale Stacks können jetzt thematisiert werden. Beispiele sind horizontale Stack-Header, die mit Buttons gefüllt sind.
<p align="center"><img width="525" height="90" alt="image" src="https://github.com/user-attachments/assets/2ed71eb1-7de2-46be-a3ce-8b8183abd8fe" /></p>

### Buttons als Balken
Neue Klassen ``button-bar-left`` und ``button-bar-right`` ermöglichen es Buttons, wie Balken auszusehen, einschließlich Icons und Statusanzeigen. Danke an [@bobzer](https://github.com/bobzer) für die Idee!
<p align="center"><img width="500" alt="image" src="https://github.com/user-attachments/assets/17f72d65-9f86-419f-b8f8-f685e64481c7" /></p>

### LCARS-Stil-Seitenleiste
Das Seitenleistenmenü hat ein LCARS-Facelift erhalten! Danke an @3of9 für diese großartige Arbeit!  
*Nicht alle Dokumentationsbilder wurden aktualisiert, um diese Ergänzung widerzuspiegeln.*
<p align="center"><img width="150" alt="themed sidebar" src="https://github.com/user-attachments/assets/b9e1e417-e597-4190-9fa8-d7d29792fb34" /></p>

### Benutzerdefinierter Text in der Kopfzeituhr
Mit einem optionalen Helper können Sie Text zur Uhr im Header hinzufügen!
<p align="center"><img width="300" alt="custom text next to the clock" src="https://github.com/user-attachments/assets/cd276787-192b-4b7a-be1e-981bd53705cd" /></p>

## Beispiele
### Dashboard
![default](https://github.com/user-attachments/assets/4c90a16c-fac8-4184-8720-a537609c0826)

### Bearbeitungsmodi
<img width="2695" height="1566" alt="image" src="https://github.com/user-attachments/assets/f11f9f0b-108b-486c-8ef1-6954696873fe" />

### Mobile Ansicht
<img width="300" alt="mobile dashboard" src="https://github.com/user-attachments/assets/958b9880-5ac7-4d7e-a519-f02b33d415d1" />
<img width="300" alt="mobile menu" src="https://github.com/user-attachments/assets/2e311e33-dad9-412c-9426-711999917b57" />

### Enthaltene Themes
<div style="display: flex; gap: 30px;">
    <img width="300" alt="classic" src="https://github.com/user-attachments/assets/f5636e72-4b21-446b-82e7-03d61e6fd6c8" />
    <img width="300" alt="25C" src="https://github.com/user-attachments/assets/4ba26e42-f965-400c-a21a-96b0d9b8160d" />
    <img width="300" alt="breen" src="https://github.com/user-attachments/assets/5487ad5c-2b1a-42b2-956e-9194b87ba226" />
    <img width="300" alt="cardassia" src="https://github.com/user-attachments/assets/b4a7b0d7-25bd-4094-bb71-1c924f4e295c" />
    <img width="300" alt="kronos" src="https://github.com/user-attachments/assets/3ffcbb74-7c46-4a7a-9bd5-f9589fa56ee3" />
    <img width="300" alt="lower decks" src="https://github.com/user-attachments/assets/470e457f-45ae-4e64-98f0-c8488ca6302c" />
    <img width="300" alt="next gen" src="https://github.com/user-attachments/assets/afbd0924-4ee8-49a1-922b-40392fba3c2d" />
    <img width="300" alt="transporter" src="https://github.com/user-attachments/assets/d2ceb6ee-f23c-4db8-b1ba-da8fd91d47ff" />
    <img width="300" alt="navigation" src="https://github.com/user-attachments/assets/ee1eb005-a09d-4c7d-a65f-ab8bca25600e" />
    <img width="300" alt="romulan" src="https://github.com/user-attachments/assets/461eaa25-ae0b-43d4-8ff9-63139e1c6b7a" />
    <img width="300" alt="red alert" src="https://github.com/user-attachments/assets/d1989f26-36f2-46a2-9df9-b3037b773a3f" />
    <img width="300" alt="blue alert" src="https://github.com/user-attachments/assets/aca17e2c-e037-4b1d-9b77-a1d3ca5411ff" />
    <img width="300" alt="yellow alert" src="https://github.com/user-attachments/assets/bc57cec2-f31b-43a3-a4cf-3cc6299763ef" />
</div>
Classic, 25th Century, Next Generation, Lower Decks, Romulus, Cardassia, Kronos, Nemesis (und mehr!).

## Präambel
Ich bin definitiv kein echter Webentwickler und habe mich mit Hilfe von Stack Exchange und verschiedenen Blogs zu CSS-Techniken irgendwie zur ersten Version durchgewurschtelt. Mein Hauptziel war und ist es, dieses Theme zu 100 % in CSS/JS zu halten, ohne zusätzliche Assets außer der Schriftart. Ich bin mir sicher, dass es bessere Wege gibt, alles umzusetzen, was ich bisher getan habe, daher sind PRs willkommen. Ich werde die Dinge weiter verbessern, während ich lerne, und mehr Kommentare in mein CSS einfügen, damit ihr nachvollziehen könnt, was die einzelnen Teile tun – und mir vielleicht sagen könnt, wie man es besser machen kann. Ich habe dieses Theme mit den meisten Standardkarten getestet, die mit Home Assistant ausgeliefert werden, sowie mit einigen aus HACS wie der Mail- und Packages-Karte. Trotzdem bin ich sicher, dass es noch Karten gibt, die stark fehlerhaft sein können. Erstellt einfach ein Issue, und ich kümmere mich darum.

## Installationsanweisungen
### Voraussetzungen
#### I. Themes aktivieren und card-mod installieren

1. Installieren Sie `card-mod` gemäß den Anweisungen auf seiner [GitHub-Seite](https://github.com/thomasloven/lovelace-card-mod "card-mod").

2. Stellen Sie sicher, dass Sie in Ihrer ``configuration.yaml``-Datei Folgendes haben:
```yaml
frontend:
  javascript_version: latest
  themes: !include_dir_merge_named themes
  extra_module_url:
    - /local/community/lovelace-card-mod/card-mod.js #or wherever you ended up putting card-mod.js
```
3. Unter dem Home Assistant **Config**-Ordner erstellen Sie einen neuen Ordner mit dem Namen **themes**.
4. **Starten** Sie Home Assistant neu, um die Änderungen zu übernehmen.

#### II. Schriftarten hinzufügen

Dieses Theme erfordert, dass Sie entweder die Schriftart `Tungsten` oder `Antonio` hinzufügen. Wenn beide verfügbar sind, verwendet das Theme Tungsten. Tungsten ist die tatsächlich in den späteren Staffeln von *Picard* verwendete Schriftart. Antonio ist sehr ähnlich und etwas weniger horizontal komprimiert. 

A. Tungsten[^1] ist für den persönlichen Gebrauch kostenlos erhältlich bei [Font Downloader](https://fontdownloader.net/tungsten-font/).  
   1. Laden Sie die Schriftdateien herunter und entpacken Sie sie  
   2. Platzieren Sie `Tungsten-Medium.woff2` und `Tungsten-Bold.woff2` in `<home-assistant-directory>/www/community/fonts/`  
   3. Laden Sie Tungsten.css vom HA-LCARS-GitHub herunter und legen Sie diese ebenfalls in `<home-assistant-directory>/www/community/fonts/` ab  
   4. Navigieren Sie zu `Settings` → `Dashboards` → `3-dot menu` → `Resources` und fügen Sie die folgenden neuen Ressourcen hinzu:  
      `/hacsfiles/fonts/tungsten.css` und wählen Sie 'stylesheet'  

##### -ODER-

B. Antonio[^2] ist über Google Fonts verfügbar und kann als Dashboard-Ressource hinzugefügt werden  
   1. Navigieren Sie zu `Settings` → `Dashboards` → `3-dot menu` → `Resources` und fügen Sie die folgenden neuen Ressourcen hinzu:  
       `https://fonts.googleapis.com/css2?family=Antonio:wght@400;700&display=swap` und wählen Sie 'stylesheet'

#### III. JavaScript-Datei hinzufügen

Dieses Theme erfordert, dass Sie eine JavaScript-Datei zu Ihren Dashboard-Ressourcen hinzufügen.

A. Navigieren Sie zu `Settings` → `Dashboards` → `3-dot menu` → `Resources` und fügen Sie die folgenden neuen Ressourcen hinzu:  
   `https://cdn.jsdelivr.net/gh/th3jesta/ha-lcars@js-main/lcars.js` und wählen Sie 'javascript'

##### -ODER-

B. Wenn Sie einer zufälligen, auf einem CDN gehosteten JavaScript-Datei nicht vertrauen (verständlich!), können Sie die Datei `lcars.js` direkt von GitHub herunterladen, selbst überprüfen und in Ihrem `<home-assistant-directory>/www/community/` ablegen. 
   - **Dies muss bei jedem HA-LCARS-Update erneut durchgeführt werden.**
   - **Fügen Sie `/local/community/lcars.js` nicht zu `extra_module_url` hinzu; es wird dort nicht funktionieren.**

> [!WARNING]
> **WENN SIE CLOUDFLARE VOR IHRER WEBSITE VERWENDEN:**  
> Leeren Sie den Site-Cache in CloudFlare (Purge Cache unter Quick Actions), wann immer Sie die lokale Datei aktualisieren oder wenn Sie den JSDelivr-Link verwenden und eine neue Version von HA-LCARS veröffentlicht wird. Dies muss sowohl bei Verwendung des JSDelivr-Links als auch bei der Ablage im www-Ordner erfolgen. Sofern nicht anders konfiguriert, cached CloudFlare alles, was auf Ihrer Website möglich ist.

#### III. Die Uhr einrichten
Damit die Uhr funktioniert, müssen Sie die Integration **Time & Date** einrichten, indem Sie Folgendes zu Ihrer configuration.yaml hinzufügen:
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

>[!NOTE]
> Möglicherweise möchten Sie diese neuen Time-&-Date-Entitäten aus der Recorder-Integration von Home Assistant entfernen, damit Ihre Datenbank nicht durch Aktualisierungen im Sekundentakt aufgebläht wird. Beispiele, wie Sie dies tun können: https://www.home-assistant.io/integrations/recorder/#common-filtering-examples

#### IV. Hilfsentitäten erstellen
Dieses Theme verfügt über Umschaltsteuerungen für Sound und Texturen, Zahlensteuerungen für die Rahmengrößen sowie einen optionalen Template-Sensor zum Hinzufügen von benutzerdefiniertem Text zur Kopfzeile. Erstellen Sie diese Hilfsentitäten, indem Sie zu ``Settings`` → ``Devices & Services`` → ``Helpers`` navigieren und zwei vom Typ **Toggle**, zwei vom Typ **Number** sowie eine vom Typ **Template** erstellen, benannt wie unten angegeben:
- LCARS Sound (Entity-ID sollte `input_boolean.lcars_sound` sein)
  - Schaltet Tasten- und Tippgeräusche ein bzw. aus
- LCARS Texture (Entity-ID sollte `input_boolean.lcars_texture` sein)
  - Schaltet ein Körnungsmuster und einen Hintergrundbeleuchtungseffekt ein bzw. aus
- LCARS Vertical (Entity-ID sollte `input_number.lcars_vertical` sein)
  - Legt die Breite der vertikalen Rahmen fest
  - Mindestwert: 26
  - Maximalwert: 60
- LCARS Horizontal (Entity-ID sollte `input_number.lcars_horizontal` sein)
  - Legt die Breite der horizontalen Rahmen fest
  - Mindestwert: 6
  - Maximalwert: 60
- Optional: LCARS Header (Entity-ID sollte `sensor.lcars_header` sein)
  - Fügt dem Uhrenbereich der Kopfzeile Text hinzu
  - Beispiel-Template: `{{ "LCARS " + states('sensor.time') }}`
<img height="276" alt="entities for LCARS sound, texture, and borders" src="https://github.com/user-attachments/assets/bc9956d6-85bb-424f-9890-dcbc4bed19d7" />

Diese Entitäten können direkt über die jeweilige Entitätsansicht gesteuert werden, oder Sie können sogar Schaltflächen zu Ihrem Dashboard hinzufügen, um sie zu steuern – genau wie bei jeder anderen Entität.


### Theme installieren
Installieren Sie es über HACS, indem Sie nach "LCARS" suchen, oder laden Sie die [neueste Version](https://github.com/th3jesta/ha-lcars/releases/latest) herunter, entpacken Sie sie und legen Sie den Ordner "lcars" in Ihren Ordner "themes".

### Theme aktivieren
#### Option 1: Über das Profil
1. Öffnen Sie Ihr Home-Assistant-**Profil**
2. Wählen Sie unter **User Settings** → **Themes** eines der neuen LCARS-Themes aus

#### Option 2: Festlegen des standardmäßigen `backend-selected`-Themes
Um dieses Theme automatisch als vom Backend ausgewähltes Standard-Theme festzulegen, fügen Sie die folgende Automation zu Ihrem Home Assistant hinzu:
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
>[!NOTE]
> Die Klassennamen dienen nur als Hinweise darauf, für welche Kartentypen sie vorgesehen waren, können jedoch auf jede beliebige Karte angewendet werden. Wie gut sie außerhalb ihres vorgesehenen Einsatzes funktionieren, kann ich jedoch nicht garantieren.

Die Klassen sind wie folgt:  

1. `header-left` `header-right` `header-contained` `header-open` – obere blaue Leiste (im Standard-Theme), gedacht für Markdown- und Heading-Karten, mit einer `H1`-Zeile, die einen Abschnitt startet  

<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>
    
```yaml
type: markdown
card_mod:
  class: header-left
content: '# header-left'

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
<img width="350" alt="ha-lcars-headers" src="https://github.com/user-attachments/assets/02d599cf-5a0b-4ad3-a20f-ff0335e34bd5" />
</td>
</tr>
</table>

2. `middle-left` `middle-right` `middle-contained` `middle-blank` – seitliche rote Leiste (im Standard-Theme), gedacht für Nicht-Button-Abschnitte unterhalb des Headers und oberhalb des Footers  

<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>
    
```yaml
type: markdown
card_mod:
  class: middle-left
content: '# middle-left'

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
<img width="350" alt="ha-lcars-middle" src="https://github.com/user-attachments/assets/691bc899-9373-4c35-90e1-de131a83f68a" />
</td>
</tr>
</table>

3. `footer-left` `footer-right` `footer-contained` `footer-open` – untere graue Leiste (im Standard-Theme), gedacht für die letzte Karte eines Abschnitts  

<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>
    
```yaml
type: markdown
card_mod:
  class: footer-left
content: '# footer-left'

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
<img width="350" alt="ha-lcars-footers" src="https://github.com/user-attachments/assets/5eb6dc12-c990-4388-bdb9-7ed08884e73c" />
</td>
</tr>
</table>

4. `button-small` – quadratische Buttons, gedacht für mittlere Abschnitte sowie horizontale Stacks und Grids  

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
<img width="107" alt="small button" src="https://user-images.githubusercontent.com/38670315/210178400-5d39e821-328f-4bd5-907d-1863dc2f7ff6.png">
</td>
</tr>
</table>

5. `button-large` – abgerundeter Button, gedacht als Einzelkarte außerhalb von Header/Middle/Footer  

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
<img width="318" alt="large button" src="https://user-images.githubusercontent.com/38670315/210178438-59da5bce-4f86-4de6-94e3-830aa845293e.png">
</td>
</tr>
</table>

6. `button-lozenge-left` `button-lozenge-right` – pillenförmige Buttons; funktionieren nur auf Standard-Button-Karten; funktionieren auch in horizontalen Stacks und Grids mit bis zu zwei Spalten, mehr Spalten führen zu Anzeigeproblemen  

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
  class: button-lozenge-left
  
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
<img width="159" alt="lozenge button" src="https://user-images.githubusercontent.com/38670315/212760869-5a09e9c0-9d61-4b48-af3c-5040a82c1722.png">
</td>
</tr>
</table>

7. `button-bullet-left` `button-bullet-right` – ähnlich wie die Lozenge-Buttons, aber eine Seite quadratisch; gleiche Spalteneinschränkungen  

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
  class: button-bullet-left
  
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
<img width="158" alt="bullet button" src="https://user-images.githubusercontent.com/38670315/212761051-a9cb1cc8-b445-46d5-9270-171249f6d63f.png">
</td>
</tr>
</table>

8. `button-capped-left` `button-capped-right` – ähnlich wie Bullet-Buttons, aber die runde Seite ist abgerundet; gleiche Spalteneinschränkungen  

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
  class: button-capped-left
  
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
<img width="164" alt="capped button" src="https://user-images.githubusercontent.com/38670315/213804819-a9949ad2-4b9c-4539-ae5a-075dec098b11.png">
</td>
</tr>
</table>
9. `button-barrel-left` `button-barrel-right` – ähnlich wie die Bullet-Buttons, aber ohne Rundungen; gleiche Spalteneinschränkungen  

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
  class: button-barrel-left
  
show_name: true
show_icon: true
type: button
tap_action:
  action: toggle
entity: switch.built_in
card_mod:
  class: button-barrel-right
```

</td>
<td>
<img width="198" alt="barrel button" src="https://github.com/user-attachments/assets/89ab1a43-276f-43b8-84f2-d6853c2940df">
</td>
</tr>
</table>

10. `button-bar-left` `button-bar-right` – Button im Stil einer Header-Leiste. Nutzt großen Text, Icon und Statusanzeige; gleiche Spalteneinschränkungen  

<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>
    
```yaml
show_name: true
show_icon: true
show_state: true
type: button
entity: light.porch_light
name: Porch
card_mod:
  class: button-bar-left

show_name: true
show_icon: true
show_state: true
type: button
entity: light.garage_light
name: Garage
card_mod:
  class: button-bar-right
```

</td>
<td>
<img width="635" height="138" alt="bar button" src="https://github.com/user-attachments/assets/17f72d65-9f86-419f-b8f8-f685e64481c7" />
</td>
</tr>
</table>

11. `bar-left` `bar-right` `bar-large-left` `bar-large-right` – eigenständige Header-Leisten; nur für Markdown- und Heading-Karten getestet. Standard- und große Versionen verfügbar, siehe [Tips & Tricks](#custom-bar-sizes) für benutzerdefinierte Größen  

<table>
<tr>
<td> YAML </td> <td> Ergebnis </td>
</tr>
<tr>
<td>
    
```yaml
type: markdown
content: 'bar-left'
card_mod:
  class: bar-left
  
type: markdown
content: 'bar-large-left'
card_mod:
  class: bar-large-left
  
type: markdown
content: 'bar-right'
card_mod:
  class: bar-right
  
type: markdown
content: 'bar-large-right'
card_mod:
  class: bar-large-right
```

</td>
<td>
<img width="689" height="181" alt="bars" src="https://github.com/user-attachments/assets/58a9f540-56f3-4b4d-acfc-02e19967fda8" />
</td>
</tr>
</table>

12. `readout-bar-right` `readout-bar-large-right` – Sensor-Anzeige: zweispaltiges Layout mit dem numerischen Wert links und dem Entitätsnamen (Beschriftung) rechts. Gedacht für `entity`-Karten (Einzelwert) und `entities`-Karten (gestapelte Sensorzeilen). Die große Variante verwendet eine größere Wertschrift. Anpassbar über die `lcars-readout-*`-Variablen (Farben, Schriftgrößen, Abstände).
<table>
<tr>
<td> YAML </td> <td> Hinweise </td>
</tr>
<tr>
<td>

```yaml
# Einzelne Entität – Standardgröße
type: entity
entity: sensor.temperature
name: TEMP
card_mod:
  class: readout-bar-right

# Einzelne Entität – groß
type: entity
entity: sensor.temperature
name: TEMP
card_mod:
  class: readout-bar-large-right

# Mehrere Sensoren gestapelt – Standardgröße
type: entities
card_mod:
  class: readout-bar-right
entities:
  - sensor.temperature
  - sensor.humidity

# Mehrere Sensoren gestapelt – groß
type: entities
card_mod:
  class: readout-bar-large-right
entities:
  - sensor.temperature
  - sensor.humidity
```

</td>
<td>

Wert (linke Spalte) zeigt den Sensorstatus in der Akzentfarbe auf dunklem Hintergrund, getrennt durch einen linken Rahmen in der Akzentfarbe. Beschriftung (rechte Spalte) zeigt den Entitätsnamen in Großbuchstaben auf der Karten-Kopffarbe. `readout-bar-large-right` verwendet eine größere Wertanzeige (`lcars-readout-large-value-font-size`, Standard `3em`).

</td>
</tr>
</table>

### Eigene Farb-Themes erstellen
Benutzerdefinierte Themes können am Ende der Datei `lcars.yaml` erstellt werden. Alternativ suchen Sie nach "===THEMES", um direkt dorthin zu springen.  
Um ein eigenes Theme zu erstellen, kopieren Sie den Abschnitt LCARS Default ans Ende der Datei und ändern die Variablen `lcars-ui-*` und `lcars-card-*` nach Belieben, unter Verwendung der Farbreferenzen am Anfang der Datei, der [LCARS Website](https://www.thelcars.com/colors.php) oder durch eigene Definitionen.

## Tipps & Tricks
>[!NOTE]
> Wenn Sie hier noch etwas hinzufügen möchten, erstellen Sie bitte ein Pull Request (PR) mit Ihrem Tipp, und ich werde ihn überprüfen, um ihn dieser Liste hinzuzufügen.
#### Stacks und Stapelung
Verwenden Sie Vertical Stack-Karten. Ob in diesem Thema oder einem anderen, sie sind unverzichtbar, um Dashboards organisiert zu halten. In LCARS sollte eine Vertical Stack-Karte zuerst eine Markdown-Karte mit dem Titel der Gruppe und der angewendeten `header`-Klasse enthalten, dann beliebig viele Karten mit der `middle`-Klasse und `button`-Klassen als einzelne Buttons oder in Horizontal Stacks oder Grids, und schließlich die `footer`-Klasse auf die letzte Karte im Vertical Stack. Diese Formation ist in allen Screenshots oben zu sehen. Beispiel:

```yaml
type: vertical-stack
cards:
  - type: markdown
    card_mod:
      class: header-left
    content: '# Climate'
  - type: weather-forecast
    entity: weather.home
    card_mod:
      class: middle-left
  - type: thermostat
    entity: climate.dining_room
    card_mod:
      class: footer-left
```

#### Button Cards im Abschnitts-Layout
Im Standard Sections-Layout von Home Assistant werden Button Cards gezwungen, zwei Reihen hoch zu sein. LCARS-Button-Themes funktionieren, sehen dann aber größer aus. Die Größe kann durch Setzen von `grid_options: rows: auto` korrigiert werden.

```yaml
type: button
show_name: true
show_icon: true
show_state: true
entity: light.front_lights
card_mod:
  class: button-lozenge-left
grid_options:
  columns: full
  rows: auto
```

#### Abschnitts-Überschriften
Standardmäßig erstellt Home Assistant am Anfang jeder Sektion eine Heading-Karte. Diese Karten können Header- und Bar-Klassen übernehmen.

```yaml
type: heading
heading_style: title
grid_options:
  columns: 18
  rows: auto
heading: LCARS Settings
icon: local:Star Trek/starfleet-star-badge
badges:
  - type: entity
    entity: input_number.lcars_horizontal
  - type: entity
    entity: input_number.lcars_vertical
  - type: entity
    entity: input_boolean.lcars_texture
card_mod:
  class: header-contained
  style: |
    :host .title { font-size: 2em;}
```

#### Leere Header
Markdown-Karten mit `## &nbsp;` als Inhalt erzeugen leere Header oder Footer. Größe kann durch Anzahl der `#` angepasst werden.

#### Schriftart auf einer einzelnen Dashboard-Karte
Für Karten, die das Theme isoliert verwenden, kann die Schriftart pro Karte mit CSS erzwungen werden:

```yaml
type: markdown
content: '# Card-level theming'
theme: LCARS Default
card_mod:
  class: header-left
  style: |
    ha-card > * {
      font-family: Antonio
    }
```

#### Selbst gehostete Fonts
Sie können Fonts selbst hosten (z.B. in einem Auto oder Air-Gapped-Netzwerk). Anleitung: [Issue #69 auf GitHub](https://github.com/th3jesta/ha-lcars/issues/69).

#### Rechtsbündiger Text
Textausrichtung kann pro Karte per CSS angepasst werden:

```yaml
card_mod:
  class: header-right
  style: |
    ha-card {
      text-align: right;
    }
```

#### Button-Hintergrundfarben
Hintergrundfarbe kann abhängig vom Lichtstatus gesetzt werden:

```yaml
card_mod:
  class: button-capped-right
  style: |
    ha-card {
      {% if is_state('light.terasa', 'on') %}
        {% set rgb_color = state_attr('light.terasa', 'rgb_color') %}
        background-color: rgba({{ rgb_color[0] }}, {{ rgb_color[1] }}, {{ rgb_color[2] }}, 1) !important;
        color: black;
      {% else %}
        background-color: #dd4444 !important;
        color: black;
      {% endif %}
    }
```

#### Benutzerdefinierte Bar-Größen
Bar-Karten können durch Skalierung der Schriftgröße angepasst werden:

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: Defiant Class Bar
    card_mod:
      class: bar-left
      style: |
        :host {
          font-size: 16px !important;
        }
  - type: markdown
    content: Constitution Class Bar
    card_mod:
      class: bar-left
  - type: markdown
    content: Galaxy Class Bar
    card_mod:
      class: bar-left
```

## Bekannte Probleme
* CSS-Stile für Font, Sidebar und Header laden nur, wenn ein Dashboard zuerst geladen wurde.
* Menü-Seiten wie Development Tools und Profile sind funktional, aber optisch eingeschränkt.
* Manchmal werden beim Laden eines Dashboards nicht alle CSS-Stile geladen und Karten sehen aus wie `button-large`. Laden Sie in diesem Fall ein kleineres Dashboard und kehren Sie zurück.

## Danksagungen
- @JHuckins: Farbsupport & Testing  
- @csanner: neue Klassen und Fixes  
- @Anthrazz: Bar-Klassen  
- @mtezzo: Toggle für Texturen/Gradienten  
- @CmdreIsaacHull: diverse Fixes und neue Klassen  
- @askpatrickw: selbst gehostete Fonts  
- @z3r0l1nk: Lichtfarben-Button Trick  
- @smugleafdev: rechtsbündiger Text  
- @Routhinator: right-footer Fix  
- @bobzer: Button-Bar Idee  
- @3of9: Sidebar & Themes  
- @adejong5: v.4 Rewrite

## Links
**Discord:** https://discord.gg/gGxud6Y6WJ  
**LCARS Resources:** https://www.thelcars.com

## Hinweis zur Urheberschaft & Haftungsausschluss

Die LCARS-Designelemente sind inspiriert von *Star Trek™* und wurden von Ressourcen auf [thelcars.com](https://www.thelcars.com) von Jim Robertus adaptiert.

Dieses Projekt ist eine nicht-kommerzielle Fanproduktion. *Star Trek* und alle zugehörigen Marken, Logos und Charaktere sind alleigentum von CBS Studios Inc. Diese Fanproduktion wird weder von CBS, Paramount Pictures noch von einer anderen *Star Trek*-Franchise unterstützt, gesponsert oder offiziell anerkannt. 

Jegliche kommerzielle Ausstellung oder Verbreitung ist nicht erlaubt. Es werden keine angeblichen unabhängigen Rechte gegenüber CBS oder Paramount Pictures geltend gemacht. Dieses Werk ist ausschließlich für den persönlichen und privaten Gebrauch bestimmt.

[^1]: Die Schriftart Tungsten wurde von Tobias Frere-Jones und Jonathan Hoefler mit Beiträgen von Sara Soskolne, Erin McLaughlin und Aoife Mooney entworfen. Tungsten ist ein eingetragenes Warenzeichen von Hoefler & Co. 

[^2]: Die Schriftart Antonio wurde von Vernon Adams entworfen und darf gemäß der SIL Open Font License, Version 1.1, frei verwendet werden.
