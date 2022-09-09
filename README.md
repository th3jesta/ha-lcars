# Home Assistant LCARS
LCARS theme for Home Assistant

Color codes and font choice from https://www.thelcars.com
    --thanks Jim Robertus!

## Installation instructions
### Prerequisites

1. Make sure that under the **configuration.yaml** file you have the following:

```
frontend:
  themes: !include_dir_merge_named themes
```

2. Under the Home Assistant **Config** folder, create a new folder named **themes**, and another folder under that called **LCARS**, then place this .yaml file therein. 
3. **Restart** Home assistant to apply the changes.

### Add the font
This theme requires you to add the `Antonio` font as a resource to your lovelace configuration:
```yaml
resources:
  - url: https://fonts.googleapis.com/css2?family=Antonio:wght@400;700&display=swap
  type: css
```
#### -OR-
Navigate to `Settings` → `Dashboards` → `3-dot menu` → `Resources` and add a new Resource with the above URL and selected as a stylesheet.

### Enable theme
1. Open your Home Assistant **Profile**
2. Under, **Themes**, select the new LCARS theme

### Setting the default `backend-selected` theme
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
      name: LCARS
    service: frontend.set_theme
```
## Usage instructions
