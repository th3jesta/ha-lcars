# Home Assistant LCARS
Star Trek LCARS theme for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration) 

<a href="https://discord.gg/gGxud6Y6WJ"><img src="https://discordapp.com/api/guilds/1059179538371858493/widget.png?style=banner2" width="140px" alt="Discord Banner 2"/></a>

Color codes and font choice from https://www.thelcars.com
    --thanks Jim Robertus!

## Examples
### Dashboard
![image](https://user-images.githubusercontent.com/38670315/212081440-039e5481-ca2b-4c08-814c-2a83d6a5a377.png "Automations for hot Earl Grey Tea not included.")

### Edit modes
![image](https://user-images.githubusercontent.com/38670315/212082080-d3543d1a-9cb2-4205-93cf-4e10829db8f8.png)

### Mobile view
<img src="https://user-images.githubusercontent.com/38670315/212080834-70b1554e-602a-42a6-8bf8-b42bf99463d5.png" width="360" /> <img src="https://user-images.githubusercontent.com/38670315/212081003-790ced32-f14d-47dc-9f13-cd711c5f02aa.png" width="360" />

### Included themes
![LCARS Themes](https://user-images.githubusercontent.com/38670315/210556056-26458f3d-60e4-400f-89df-f0b8cc68a6a2.png)
Classic, Lower Decks, Romulus, Cardassia, Kronos, Nemesis.
    
## Preamble
I am most definitely not a real web developer, and fumbled my way into the initial release with the help of Stack Exchange and various blogs on CSS techniques. My main goal was and still is to keep this theme 100% CSS with no extra assets required besides the font. I'm positive there are better ways to implement anything and everything I've done thus far, so PRs are welcome. I will continue to improve things as I learn and add more comments to my CSS so that you can know what things do and maybe tell me how it can be better if you know. I have tested this theme with most of the out-of-the-box cards that ship with Home Assistant, and some available in HACS like the Mail and Packages card. However, I'm sure there are some that could still be terribly broken. Simply create an issue and I will address it. 

## Installation instructions
### Prerequisites
#### I. Enable themes and install card-mod

1. Install `card-mod` per the instructions on its [GitHub page](https://github.com/thomasloven/lovelace-card-mod "card-mod").

2. Make sure in your **configuration.yaml** file you have the following:
```yaml
frontend:
  javascript_version: latest
  themes: !include_dir_merge_named themes
  extra_module_url:
    - /local/community/lovelace-card-mod/card-mod.js #or wherever you ended up putting card-mod.js
```
3. Under the Home Assistant **Config** folder, create a new folder named **themes**. 
4. **Restart** Home assistant to apply the changes.

#### II. Add the font
This theme requires you to add the `Antonio` font as a resource to your lovelace configuration:
```yaml
resources:
  - url: https://fonts.googleapis.com/css2?family=Antonio:wght@400;700&display=swap
    type: css
```
##### -OR-
Navigate to `Settings` → `Dashboards` → `3-dot menu` → `Resources` and add a new Resource with the above URL and selected as a stylesheet.

#### III. Set up the clock
In order for the clock to work, you need to set up the Time & Date integration by adding the following to your configuration.yaml:
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
      - 'beat'
```

More info:
https://www.home-assistant.io/integrations/time_date/

### Install the theme
Install via HACS by searching "LCARS" or download the [latest release](https://github.com/th3jesta/ha-lcars/releases/latest) and extract and drop the lcars folder into your themes folder.

### Enable theme
#### Option 1: Via profile
1. Open your Home Assistant **Profile**
2. Under, **Themes**, select one of the new LCARS themes
3. Call the `frontend.reload_themes` service.

#### Option 2: Setting the default `backend-selected` theme
In order to have this theme set automatically as the backend selected default, add the following automation to your Home Assistant:
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
## Usage instructions
### Classes
The theme includes some classes that can be added to cards like this to give them special styling:
```yaml
card_mod:
  class: header
```
_The class names are only indications of what types of cards they were intended for, but the classes can be applied to any card you like. I cannot guarantee how well they will work outside of their intended uses, however._

The classes are as follows:
1. `header` `header-right` `header-contained` `header-open` - top blue bar (in Default theme) meant for Markdown cards with one `H1` line that will start a section
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

2. `middle` `middle-right` `middle-contained` -  side red bar (in Default theme) meant for non-button sections below `header` and above `footer`
<table>
<tr>
<td> YAML </td> <td> Result </td>
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
```

</td>
<td>
<img width="315" alt="image" src="https://user-images.githubusercontent.com/38670315/212480611-018e7de1-71dc-45e6-8f55-48b82b4dd04d.png">
</td>
</tr>
</table>

3. `middle-blank` - special case for Mushroom Cards (@csanner please confirm)

4. `footer` `footer-right` `footer-contained` `footer-open` - bottom gray bar (in Default theme) meant for the last card in a section
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

5. `button-small` - squared off buttons intended to go in middle sections and horizontal-stacks and grids
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

6. `button-large` - rounded button meant to be standalone outside of `header`/`middle`/`footer` sections
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

7. `button-lozenge` `button-lozenge-right` - pill-shaped button; only works on standard button cards; also works on button cards in a horizontal-stacks and grids up to two columns wide; more columns get glitchy and is not advised
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

8. `button-bullet` `button-bullet-right` - similar to the lozenge, but with a squared-off side; same column restrictions apply
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

9. `button-capped` `button-capped-right` - similar to the bullet, but capped on the round side; same column restrictions apply
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

10. `bar` `bar-right` `bar-large` `bar-large-right` - standalone header-type bar; only intended for and tested with Markdown cards
<table>
<tr>
<td> YAML </td> <td> Result </td>
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


### Make your own color themes
Custom themes can be created down at the bottom of `lcars.yaml`. Or, search for "===THEMES", which will take you right there. To create your own theme, copy the LCARS Default section to the bottom of the file and change the `lcars-ui-*` and `lcars-card-*` variables to your liking, using the color references at the top of the file, [The LCARS website](https://www.thelcars.com/colors.php), or define your own.

### Noise and gradients
If you're not feeling the subtle noise and gradients that this theme added, let me know by raising an issue. I am still working on an easy method to enable and disable them. You can remove them yourself by searching for "base64" and "-gradient" (you should find 3 entries each) and commenting/deleting the entire CSS blocks that contain them. [Feature request here](https://github.com/th3jesta/ha-lcars/issues/5).

## Tips and tricks
_If you have anything to add here, create a PR with your tip and I will review it to add to this list._
* Make use of Vertical Stack cards. Whether in this theme or any other theme, they are invaluable for keeping dashboards organized. In LCARS, a Vertical Stack card should contain a Markdown card first with the title of the group and the `header` class applied, then any number of `middle` class cards and `button` class single buttons or in horizontal stacks or grids, and then finally a `footer` class applied to the last card in the vertical stack. You can see this formation in all of the screenshots at the top of this page. Here's an example Vertical Stack card and all of its contents:
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

* You can create a blank header or footer by creating a Markdown card and putting `## &nbsp;` in the Content field, and change the size by modifying the number of `#`. It looks like this:
![image](https://user-images.githubusercontent.com/38670315/210792537-f25c740d-1ad3-4ac7-8a31-59ad04cf38fb.png)


## Known issues
* Font and sidebar and header CSS styles only load when a dashboard has been loaded first. If you navigate directly to a non-dashboard page without loading a dashboard first, things will look pretty awful, though still functional. Simply load a dashboard and hit the back button. This is a quirk of the [card-mod](https://github.com/thomasloven/lovelace-card-mod) addon on which this theme relies, so it's outside my ability to fix.
* card-mod classes do not work with Vertical Stack and Horizontal Stacks cards (though they do work with the cards they contain). This is a quirk of the [card-mod](https://github.com/thomasloven/lovelace-card-mod) addon on which this theme relies, so it's outside my ability to fix. There is, however, a hacky workaround I have identified though have opted to not include at this time. Please submit a feature request if you would like to see this included.
* ~~Collapsing and expanding the sidebar or zooming the interface will jack with the noise and gradient overlays. A simple refresh will set everything right again. I hope to find a way to make the pseudo elements that contain the textures to dynamically adjust with the DOM. PRs are welcome. [Bug here](https://github.com/th3jesta/ha-lcars/issues/4).~~
* Menu pages like Development Tools and Profile are functional, but not great. Unfortunately, there's not much I can do to address this as card-mod does not provide a method to change these pages. Issues raised for anything comepletely broken and unsuable that I may have missed are welcome, as are PRs to make to make things better.
* Sometimes when a dashboard loads, not all CSS styles will load and all or most cards will end up looking like the `button-large` cards. This is more prevalent on large dashboards. Try reloading the page, and if that doesn't work, load a smaller dashboard and then go back to the offending dashboard.

## Acknowledgements
- Thanks to @JHuckins for color theming support and testing!
- Thanks to @csanner for the new classes and additional fixes and tweaks!
- Thanks to @Anthrazz for the bar classes!

## Links
**Discord:** https://discord.gg/gGxud6Y6WJ

**LCARS Resources:** https://www.thelcars.com
