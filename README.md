# Home Assistant LCARS
Star Trek LCARS theme for Home Assistant



## Example dashboard
![image](https://user-images.githubusercontent.com/38670315/206508333-b9f5dbed-8eea-4cf6-94d7-22289d2c531b.png "Automations for hot Earl Grey Tea not included.")
Color codes and font choice from https://www.thelcars.com
    --thanks Jim Robertus!
    
## Included themes
![image](https://user-images.githubusercontent.com/38670315/206508344-043c00ad-2407-4159-a1ee-1800dbea3e2a.png "Classic, Lower Decks, Nemesis, Romulus, Kronos.")
    
## Preamble
I am most definitely not a real web developer, and fumbled my way into this initial release with the help of Stack Exchange and various blogs on CSS techniques. My main goal was and still is to keep this theme 100% CSS with no extra assets required besides the font. I'm positive there are better ways to implement anything and everything I've done thus far, so PRs are welcome. I will continue to improve things as I learn and add more comments to my CSS so that you can know what things do and maybe tell me how it can be better if you know. I have tested this theme with most of the out-of-the-box cards that ship with Home Assistant, and some available in HACS like the Mail and Packages card. However, I'm sure there are some that could still be terribly broken. Simply create an issue and I will address it. 

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
    - /local/community/card-mod.js #or wherever you ended up putting card-mod.js
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
Install via HACS (pending) or download and drop the lcars folder into your themes folder.

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
The theme includes 6 classes that can be added to cards like this to give them special styling:
```yaml
card-mod:
  class: header
```
Those classes are as follows
1. `header` - top blue bar (in Default theme) meant for Markdown cards with one `H1` line that will start a section
2. `middle` -  side red bar (in Default theme) meant for non-button sections below `header` and above `footer`
3. `footer` - bottom gray bar (in Default theme) meant for the last card in a section
4. `button-small` - squared off buttons intended to go in middle sections
5. `button-large` - rounded button meant to be standalone outside of `header`-`middle`-`footer` sections
6. `button-lozenge` - pill-shaped button; only works on standard button cards in a horizontal-stack card that's two columns wide

### Make your own color themes
Custom themes can be created down at the bottom of `lcars.yaml`. Or, search for "===THEMES", which will take you right there. To create your own theme, copy the LCARS Default section to the bottom of the file and change the `lcars-ui-*` and `lcars-card-*` variables to your liking, using the color references at the top of the file, [The LCARS website](https://www.thelcars.com/colors.php), or define your own.

### Noise and gradients
If you're not feeling the subtle noise and gradients that this theme added, let me know by raising an issue. I am still working on an easy method to enable and disable them. You can remove them yourself by searching for "base64" (you should find 3 entries) and commenting/deleting the entire CSS blocks that contains them. [Feature request here](https://github.com/th3jesta/ha-lcars/issues/5).

## Known issues
* Collapsing and expanding the sidebar or zooming the interface will jack with the noise and gradient overlays. A simple refresh will set everything right again. I hope to find a way to make the pseudo elements that contain the textures to dynamically adjust with the DOM. PRs are welcome. [Bug here](https://github.com/th3jesta/ha-lcars/issues/4).
* Mobile interface is 100% functional, though could still use some styling to correct things like the odd positioning of the Home Assistant header in the sidebar. It's in my list of improvements to implement. PRs are welcome. [Bug here](https://github.com/th3jesta/ha-lcars/issues/6).
* Menu pages like Development Tools and Profile are functional, but not great. Unfortunately, there's not much I can do to address this as card-mod does not provide a method to change these pages. Issues raised for anything comepletely broken and unsuable that I may have missed are welcome, as are PRs to make to make things better.

## Acknowledgements
Thanks to @JHuckins for color theming support!
