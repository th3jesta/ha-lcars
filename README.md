# Home Assistant LCARS
Star Trek LCARS theme for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration) 

<a href="https://discord.gg/gGxud6Y6WJ"><img src="https://discordapp.com/api/guilds/1059179538371858493/widget.png?style=banner2" width="140px" alt="Discord Banner 2"/></a>

Color codes and font choice from https://www.thelcars.com
    --thanks Jim Robertus!

# 💥BREAKING CHANGES IN 4.0💥
1. Home Assistant LCARS is built using the functionality of [card-mod](https://github.com/thomasloven/lovelace-card-mod "card-mod"). Version 4.x of card-mod includes numerous breaking changes to all themes, including Home Assistant LCARS. Most standard cards using this theme should update without any issues. Any cards with custom css applied using ``card-mod: style:`` may need to be manually updated to card-mod's new element selectors (i.e. ``hui-card`` instead of ``ha-card``). See card-mod's [README](https://github.com/thomasloven/lovelace-card-mod/blob/master/README.md) and [README-application](https://github.com/thomasloven/lovelace-card-mod/blob/master/README-application.md) as starting points.
2. Because of the changes mentioned above, a few cards are no longer supported or need a special workaround. The workaround is to place the card inside a vertical or horizontal stack. This changes how card-mod sees the card and applies the theme. Cards known to have issues include:
   - ⚠️ custom-button-card: stack workaround required for some theme classes. Apply the desired theme class to the stack. Use Custom Button Cards style capabilities to make the button look how you want it.
3. Bar cards can now be scaled by changing the font size of the card (see [Tips and Tricks](#custom-bar-sizes) below). Because of this, the markdown **must not** include any font sizing, such as the header ``#``.
4. This is an almost complete rewrite, including several css optimizations. Dashboards designed using previous versions may need to be updated slightly due to small changes in spacing and padding. 

# 🎉NEW FEATURES IN 4.0🎉
### Themed stacks 
Vertical and horizontal stacks can now be themed. Examples include a horizontal stack header filled with buttons
<p align="center"><img width="525" height="90" alt="image" src="https://github.com/user-attachments/assets/2ed71eb1-7de2-46be-a3ce-8b8183abd8fe" /></p>

### Buttons as bars
New classes ``button-bar-left`` and ``button-bar-right`` allow buttons to appear like the bars, including icons and states. Thanks [@bobzer](https://github.com/bobzer) for the idea!
<p align="center"><img width="500" alt="image" src="https://github.com/user-attachments/assets/17f72d65-9f86-419f-b8f8-f685e64481c7" /></p>

### LCARS Style Sidebar
The sidebar menu has been given a LCARS facelift! Thanks @3of9 for this stunning work!  
*Not all of the documentation images have been updated to reflect this addition.*
<p align="center"><img width="150" alt="themed sidebar" src="https://github.com/user-attachments/assets/b9e1e417-e597-4190-9fa8-d7d29792fb34" /></p>

### Custom text in the header clock
Using an optional helper, you can add text to the header clock!
<p align="center"><img width="300" alt="custom text next to the clock" src="https://github.com/user-attachments/assets/cd276787-192b-4b7a-be1e-981bd53705cd" /></p>

## Examples
### Dashboard
![default](https://github.com/user-attachments/assets/4c90a16c-fac8-4184-8720-a537609c0826)

### Edit modes
<img width="2695" height="1566" alt="image" src="https://github.com/user-attachments/assets/f11f9f0b-108b-486c-8ef1-6954696873fe" />


### Mobile view
<img width="300" alt="mobile dashboard" src="https://github.com/user-attachments/assets/958b9880-5ac7-4d7e-a519-f02b33d415d1" />
<img width="300" alt="mobile menu" src="https://github.com/user-attachments/assets/2e311e33-dad9-412c-9426-711999917b57" />

### Included themes
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
Classic, 25th Century, Next Generation, Lower Decks, Romulus, Cardassia, Kronos, Nemesis (and more!).
    
## Preamble
I am most definitely not a real web developer, and fumbled my way into the initial release with the help of Stack Exchange and various blogs on CSS techniques. My main goal was and still is to keep this theme 100% CSS/JS with no extra assets required besides the font. I'm positive there are better ways to implement anything and everything I've done thus far, so PRs are welcome. I will continue to improve things as I learn and add more comments to my CSS so that you can know what things do and maybe tell me how it can be better if you know. I have tested this theme with most of the out-of-the-box cards that ship with Home Assistant, and some available in HACS like the Mail and Packages card. However, I'm sure there are some that could still be terribly broken. Simply create an issue and I will address it. 

## Installation instructions
### Prerequisites
#### I. Enable themes and install card-mod

1. Install `card-mod` per the instructions on its [GitHub page](https://github.com/thomasloven/lovelace-card-mod "card-mod").

2. Make sure in your ``configuration.yaml`` file you have the following:
```yaml
frontend:
  themes: !include_dir_merge_named themes
  extra_module_url:
    - /www/community/lovelace-card-mod/card-mod.js?hacstag=1234567890 #or wherever you put card-mod
```
3. Under the Home Assistant ``config`` folder, create a new folder named ``themes``   
4. **Restart** Home assistant to apply the changes.

#### II. Add the fonts

This theme requires you to add either the `Tungsten` font or the `Antonio` font. If both are available, the theme will use Tungsten. Tungsten is the actual font used in the later seasons of *Picard*. Antonio is a very similar and is slightly less horizontally compressed. 

A. Tungsten[^1] is available free for personal use from [Font Downloader](https://fontdownloader.net/tungsten-font/).  
   1. Download and unzip the font files  
   2. Place `Tungsten-Medium.woff2` and `Tungsten-Bold.woff2` in `<home-assistant-directory>/www/community/fonts/`  
   3. Download Tungsten.css from the HA-LCARS GitHub and place it also in `<home-assistant-directory>/www/community/fonts/`  
   4. Navigate to `Settings` → `Dashboards` → `3-dot menu` → `Resources` and add the following new Resources:  
      `/hacsfiles/fonts/tungsten.css` and select 'stylesheet'  

##### -OR-

B. Antonio[^2] is available from Google Fonts and can be added as a Dashboard Resource
   1. Navigate to `Settings` → `Dashboards` → `3-dot menu` → `Resources` and add the following new Resources:  
       `https://fonts.googleapis.com/css2?family=Antonio:wght@400;700&display=swap` and select 'stylesheet'

#### III. Add the Javascript file

This theme requires you to add a javascript file to your Dashboard Resources

A. Navigate to `Settings` → `Dashboards` → `3-dot menu` → `Resources` and add the following new Resources:  
   `https://cdn.jsdelivr.net/gh/th3jesta/ha-lcars@js-main/lcars.js` and select javascript

##### -OR-

B. If you don't trust someone's random JavaScript hosted on a CDN (I get it), you can download the `lcars.js` file directly from GitHub, audit it yourself, and place it in your `<home-assistant-directory>/www/community/`. 
   - **This will need to be done with every HA-LCARS update.**
   - **Do not add `/local/community/lcars.js` to `extra_module_url`; it will not work there.**

> [!WARNING]
> **IF YOU USE CLOUDFLARE IN FRONT OF YOUR SITE:**  
> Purge your site cache in CloudFlare (Purge Cache under Quick Actions) anytime you update the local file or if you are using the JSDelivr link and a new version of HA-LCARS is released. This needs to happen whether you are using the JSDelivr link or putting it in your www folder. Unless you tell it not to, CloudFlare caches anything in your site that it can.
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
```

More info:
https://www.home-assistant.io/integrations/time_date/

> [!NOTE]  
> You may wish to remove these new Time & Date entities from Home Assistant's Recorder integration so they don't fill you database with updates every second. Examples on how to do that: https://www.home-assistant.io/integrations/recorder/#common-filtering-examples


#### IV. Create the helper entities
This theme has toggle controls for sound and textures, number controls for border sizes, and an optional template sensor for adding custom text to the header. Create these helper entities by going to ``Settings`` → ``Devices & Services`` → ``Helpers`` and create two of type **Toggle**, two of type **Number**, and one of type **Template** named as below:
- LCARS Sound (entity id should be `input_boolean.lcars_sound`)
  - Toggles button and tap sounds 
- LCARS Texture (entity id should be `input_boolean.lcars_texture`)
  - Toggles a grain pattern and backlight effect 
- LCARS Vertical (entity id should be `input_number.lcars_vertical`)
  - Sets the width of vertical borders
  - Min value: 26
  - Max value: 60
- LCARS Horizontal (entity id should be `input_number.lcars_horizontal`)
  - Sets the width of horizontal borders
  - Min value: 6
  - Max value: 60
- Optional: LCARS Header (entity id should be `sensor.lcars_header`)
  - Add text to the clock area of the header
  - Example Template: `{{ "LCARS " + states('sensor.time') }}`
<img height="276" alt="entities for LCARS sound, texture, and borders" src="https://github.com/user-attachments/assets/bc9956d6-85bb-424f-9890-dcbc4bed19d7" />

These entities can be controlled directly from viewing the entity, or you can even add buttons to your dashboard to control them, just like any other entity. 

### Install the theme
Install via HACS by searching "LCARS" or download the [latest release](https://github.com/th3jesta/ha-lcars/releases/latest) and extract and drop the lcars folder into your themes folder.

### Enable theme
#### Option 1: Via profile
1. Open your Home Assistant **Profile**
2. Under **User Settings** → **Themes**, select one of the new LCARS themes

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
  class: header-left
```
> [!NOTE]  
> The class names are only indications of what types of cards they were intended for, but the classes can be applied to any card you like. I cannot guarantee how well they will work outside of their intended uses, however.

The classes are as follows:
1. `header-left` `header-right` `header-contained` `header-open` - top blue bar (in Default theme) meant for Markdown and Heading cards and with one `H1` line that will start a section
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

2. `middle-left` `middle-right` `middle-contained` `middle-blank` -  side red bar (in Default theme) meant for non-button sections below `header` and above `footer`
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

3. `footer-left` `footer-right` `footer-contained` `footer-open` - bottom gray bar (in Default theme) meant for the last card in a section
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

4. `button-small` - squared off buttons intended to go in middle sections and horizontal-stacks and grids
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
<img width="107" alt="small button" src="https://user-images.githubusercontent.com/38670315/210178400-5d39e821-328f-4bd5-907d-1863dc2f7ff6.png">
</td>
</tr>
</table>

5. `button-large` - rounded button meant to be standalone outside of `header`/`middle`/`footer` sections
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
<img width="318" alt="large button" src="https://user-images.githubusercontent.com/38670315/210178438-59da5bce-4f86-4de6-94e3-830aa845293e.png">
</td>
</tr>
</table>

6. `button-lozenge-left` `button-lozenge-right` - pill-shaped button; only works on standard button cards; also works on button cards in a horizontal-stacks and grids up to two columns wide; more columns get glitchy and is not advised
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

7. `button-bullet-left` `button-bullet-right` - similar to the lozenge, but with a squared-off side; same column restrictions apply
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

8. `button-capped-left` `button-capped-right` - similar to the bullet, but capped on the round side; same column restrictions apply
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

9. `button-barrel-left` `button-barrel-right` - similar to the bullet, but no rounding at all; same column restrictions apply
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

9. `button-bar-left` `button-bar-right` - button in the style of a header bar. Uses large text and includes the icon and state of shown; same column restrictions apply
<table>
<tr>
<td> YAML </td> <td> Result </td>
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

10. `bar-left` `bar-right` `bar-large-left` `bar-large-right` - standalone header-type bar; only intended for and tested with Markdown and Heading cards. Comes with a standard and large versions, see [Tips & Tricks](#custom-bar-sizes) for custom sizing
<table>
<tr>
<td> YAML </td> <td> Result </td>
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


### Make your own color themes
Custom themes can be created down at the bottom of `lcars.yaml`. Or, search for "===THEMES", which will take you right there. To create your own theme, copy the LCARS Default section to the bottom of the file and change the `lcars-ui-*` and `lcars-card-*` variables to your liking, using the color references at the top of the file, [The LCARS website](https://www.thelcars.com/colors.php), or define your own.

## Tips and tricks
> [!NOTE]  
> If you have anything to add here, create a PR with your tip and I will review it to add to this list.

#### Stacks and stacks and stacks
Make use of Vertical Stack cards. Whether in this theme or any other theme, they are invaluable for keeping dashboards organized. In LCARS, a Vertical Stack card should contain a Markdown card first with the title of the group and the `header` class applied, then any number of `middle` class cards and `button` class single buttons or in horizontal stacks or grids, and then finally a `footer` class applied to the last card in the vertical stack. You can see this formation in all of the screenshots at the top of this page. Here's an example Vertical Stack card and all of its contents:
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

</td>
<td>
<img width="308" alt="stack with themed cards" src="https://user-images.githubusercontent.com/38670315/210189965-b73662a8-5390-46ea-9450-b0043e6d2547.png">
</td>
</tr>
</table>

Additionally, since version 4.0, vertical and horizontal stacks can be themed. This allows multiple cards to be stacked evenly within LCARS framing:
<table>
<tr>
<td> YAML </td> <td> Result </td>
</tr>
<tr>
<td>
    
```yaml
type: vertical-stack
grid_options:
  columns: 48
  rows: auto
card_mod:
  class: header-left
cards:
  - type: heading
    heading_style: title
    heading: Stack Example
    icon: fa6-solid:cubes-stacked
    badges:
      - type: entity
        entity: input_number.lcars_horizontal
      - type: entity
        entity: input_number.lcars_vertical
      - type: entity
        entity: input_boolean.lcars_texture
    card_mod:
      style: ":host .title {font-size:2em;}"
  - type: horizontal-stack
    card_mod:
      class: header-right
    cards:
      - show_name: true
        show_icon: true
        type: button
        entity: light.east_flood_lights
        card_mod:
          class: button-lozenge-left
      - show_name: true
        show_icon: true
        type: button
        entity: light.south_flood_lights
        card_mod:
          class: button-lozenge-right
  - type: horizontal-stack
    card_mod:
      class: middle-right
    cards:
      - show_name: true
        show_icon: true
        type: button
        entity: light.porch_light
        card_mod:
          class: button-lozenge-left
      - show_name: true
        show_icon: true
        type: button
        entity: light.garage_light
        card_mod:
          class: button-lozenge-right
  - type: horizontal-stack
    card_mod:
      class: footer-right
    cards:
      - show_name: true
        show_icon: true
        type: button
        entity: light.front_lights
        card_mod:
          class: button-lozenge-left
      - show_name: true
        show_icon: true
        type: button
        entity: light.stoop_light
        card_mod:
          class: button-lozenge-right
```

</td>
<td>
<img width="1048" height="321" alt="themed stacks" src="https://github.com/user-attachments/assets/cafc28e0-2a90-4062-8bd4-7a3a6f25ae40" />
</td>
</tr>
</table>

#### Button Cards in Section Layout
When using Home Assistant's Sections layout (currently the default for new dashboards), button cards are forced to be two rows tall. While LCARS button themes will work, they will look bigger than in the examples. The size can be corrected by setting the ``grid_options: rows: auto`` as such:  

<table>
<tr>
<td> YAML </td> <td> Result </td>
</tr>
<tr>
<td>
    
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

</td>
<td>
<img width="518" height="200" alt="multirow buttons" src="https://github.com/user-attachments/assets/3c6827e9-daa8-46ed-9a09-3bf326a3c818" />
</td>
</tr>
</table>

#### Section Layout Headings
By default, Home Assistant creates a Heading Card at the top of each Section. This card can take the header and bar classes!

<table>
<tr>
<td> YAML </td> <td> Result </td>
</tr>
<tr>
<td>
    
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

type: heading
icon: local:Star Trek/starfleet-star-badge
heading: LCARS Settings
heading_style: title
badges:
  - type: entity
    entity: input_number.lcars_vertical
  - type: entity
    entity: input_number.lcars_horizontal
  - type: entity
    entity: input_boolean.lcars_texture
card_mod:
  class: bar-left
grid_options:
  columns: 18
  rows: auto
```

</td>
<td>
<img width="793" height="116" alt="section headings" src="https://github.com/user-attachments/assets/b88d95a4-9f2a-4147-81e9-dafb2e09bc75" />

</td>
</tr>
</table>

#### Blank Headers
You can create a blank header or footer by creating a Markdown card and putting `## &nbsp;` in the Content field, and change the size by modifying the number of `#`. It looks like this:
![image](https://user-images.githubusercontent.com/38670315/210792537-f25c740d-1ad3-4ac7-8a31-59ad04cf38fb.png)

#### Font on a single dashboard
If you are only applying the theme to a dashboard or a card, the font won't render on the cards. You can brute-force loading the font on a per-card basis by adding the following style to every card:
<table>
<tr>
<td> YAML </td> <td> Result </td>
</tr>
<tr>
<td>
    
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

</td>
<td>
<img width="308" alt="themed card" src="https://user-images.githubusercontent.com/38670315/236198970-0c06be57-d331-41d8-b692-95741b68bf5e.png">
</td>
</tr>
</table>

#### Font on air-gapped installs
If you want to host the font yourself, such as running a Home Assistant instance in a car or on an air-gapped network, you can learn how to download the font and install it from issue https://github.com/th3jesta/ha-lcars/issues/69.

#### Right-aligned text
You can switch the alignment of text in a card, such as the markdown card for `header-right`, by adding custom CSS per card like so:
<table>
<tr>
<td> YAML </td> <td> Result </td>
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
<img width="308" alt="header with right aligned text" src="https://github.com/th3jesta/ha-lcars/assets/38670315/41c38e14-5041-4355-8581-07c82c96ceca">
</td>
</tr>
</table>

#### Button Background Colors
You can set a button's background color to the color of the light by adding custom CSS per card like so:
<table>
<tr>
<td> YAML </td> <td> Result </td>
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
        background-color: rgba({{ rgb_color[0] }}, {{ rgb_color[1] }}, {{ rgb_color[2] }}, 1) !important;
        color: black;  /* or any other logic for text color */
      {% else %}
        background-color: #dd4444 !important;
        color: black;
      {% endif %}
    }
```

</td>
<td>
<img width="308" alt="buttons with state-dependent background colors" src="https://github.com/th3jesta/ha-lcars/assets/38670315/8417b463-0d0b-447d-8a7b-374d47f1e251">

</td>
</tr>
</table>

#### Custom Bar Sizes
You can the size of a bar card by scaling the font size of the card like so:
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

</td>
<td>
<img width="793" height="135" alt="bars with various sizes" src="https://github.com/user-attachments/assets/d1d992b0-608e-43f0-b17a-614b7a366435" />
</td>
</tr>
</table>

## Known issues
* Font and sidebar and header CSS styles only load when a dashboard has been loaded first. If you navigate directly to a non-dashboard page without loading a dashboard first, things will look pretty awful, though still functional. Simply load a dashboard and hit the back button. This is a quirk of the [card-mod](https://github.com/thomasloven/lovelace-card-mod) addon on which this theme relies, so it's outside my ability to fix.
* Menu pages like Development Tools and Profile are functional, but not great. Unfortunately, there's not much I can do to address this as card-mod does not provide a method to change some of these pages. Issues raised for anything comepletely broken and unsuable that I may have missed are welcome, as are PRs to make to make things better.
* Sometimes when a dashboard loads, not all CSS styles will load and all or most cards will end up looking like the `button-large` cards. This is more prevalent on large dashboards. Try reloading the page, and if that doesn't work, load a smaller dashboard and then go back to the offending dashboard.

## Acknowledgements
- Thanks to @JHuckins for color theming support and testing!
- Thanks to @csanner for the new classes and additional fixes and tweaks!
- Thanks to @Anthrazz for the bar classes!
- Thanks to @mtezzo for the entity toggle for textures/gradients, and the Modern theme (my new favorite)!
- Thanks to @CmdreIsaacHull for various fixes, improvements, themes, and new classes!
- Thanks to @askpatrickw for figuring out how to self-host the font!
- Thanks to @z3r0l1nk for light color-matching button trick!
- Thanks to @smugleafdev for the right-justified text tip!
- Thanks to @Routhinator (via Discord) for the right-footer fix!
- Thanks to @bobzer for the button-bar idea!
- Thanks to @3of9 for the sidebar and themes!
- Thanks to @adejong5 for the v.4 rewrite!

## Links
**Discord:** https://discord.gg/gGxud6Y6WJ

**LCARS Resources:** https://www.thelcars.com

## Attribution & Disclaimer

LCARS design elements inspired by *Star Trek™* and adapted from resources at [thelcars.com](https://www.thelcars.com) by Jim Robertus.

This project is a non-commercial fan production. *Star Trek* and all related marks, logos, and characters are solely owned by CBS Studios Inc. This fan production is not endorsed by, sponsored by, nor affiliated with CBS, Paramount Pictures, or any other *Star Trek* franchise. 

No commercial exhibition or distribution is permitted. No alleged independent rights will be asserted against CBS or Paramount Pictures. This work is intended for personal and recreational use only.

[^1]: Tungsten is designed by Tobias Frere-Jones and Jonathan Hoefler with contributions from Sara Soskolne, Erin McLaughlin, and Aoife Mooney. Tungsten is a registered trademark of Hoefler & Co. 
[^2]: Antonio is designed by Vernon Adams and is free to use in accordance with the SIL Open Font License, Version 1.1.
