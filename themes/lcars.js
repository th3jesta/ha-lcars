class SidebarCustomStyle {
  refs = {
    ha: null,
    main: null,
    drawer: null
  }

  constructor() {
    try {
      this.refs.ha = document.querySelector("home-assistant")
      console.info(`%c  home-assistant:  ${this.refs.ha}  `, "color: #ff9800; font-weight: bold; background-color: black")
      this.refs.main = this.refs.ha?.shadowRoot.querySelector("home-assistant-main")?.shadowRoot
      console.info(`%c  home-assistant-main: ${this.refs.main}  `, "color: #ff9800; font-weight: bold; background-color: black")
      this.refs.drawer = this.refs.main?.querySelector("ha-drawer")?.shadowRoot
      this.run()
    } catch (ex) { }
  }

  run = () => {
    console.info(`%c  SIDEBAR BORDER HAS BEEN REMOVED  `, "color: #ff9800; font-weight: bold; background-color: black")
    setTimeout(() => {
      try {
        this.refs.drawer.querySelector("aside").style.borderRightStyle = "unset"
      } catch(error) { }
    }, 1)
  }
}

Promise.resolve(customElements.whenDefined('paper-listbox')).then(() => {
  console.info(`%c  REMOVING SIDEBAR BUTTON  `, "color: #ff9800; font-weight: bold; background-color: black")
  window.customStyle = new SidebarCustomStyle()
})

const btnBeep = new Audio("data:audio/mpeg;base64,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");
class BtnSoundEffects {
  refs = {
    ha: null,
    main: null,
    drawer: null,
    resolver: null,
    lovelace: null,
    root: null,
    view: null,
    hui: null,
    masonry: null,
    columns: null,
    columnsList: null
  }

  constructor() {
    try {
      this.refs.ha = document.querySelector("home-assistant")
      console.info(`%c  home-assistant:  ${this.refs.ha}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.refs.main = this.refs.ha?.shadowRoot.querySelector("home-assistant-main")?.shadowRoot
      console.info(`%c  home-assistant-main: ${this.refs.main}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.refs.drawer = this.refs.main?.querySelector("ha-drawer")
      console.info(`%c  ha-drawer: ${this.refs.drawer}  `, "color: #ff9800; font-weight: bold; background-color: black")

      this.refs.resolver = this.refs.drawer?.querySelector("partial-panel-resolver")
      console.info(`%c  partial-panel-resolver: ${this.refs.resolver}  `, "color: #ff9800; font-weight: bold; background-color: black")
////////////////////////////////////
      this.refs.lovelace = this.refs.resolver?.querySelector("ha-panel-lovelace")?.shadowRoot
      console.info(`%c  ha-panel-lovelace: ${this.refs.lovelace}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.refs.root = this.refs.lovelace?.shadowRoot.querySelector("hui-root")?.shadowRoot
      console.info(`%c  hui-root: ${this.refs.root}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.refs.view = this.refs.root?.shadowRoot.querySelector("#view")?.shadowRoot
      console.info(`%c  #view: ${this.refs.view}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.refs.hui = this.refs.view?.shadowRoot.querySelector("hui-view")?.shadowRoot
      console.info(`%c  hui-view: ${this.refs.hui}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.refs.masonry = this.refs.hui?.shadowRoot.querySelector("hui-masonry-view")?.shadowRoot
      console.info(`%c  hui-masonry-view: ${this.refs.masonry}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.refs.columns = this.refs.masonry?.shadowRoot.querySelector("#columns")
      console.info(`%c  #columns: ${this.refs.columns}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.refs.columnsList = this.refs.columns?.querySelectorAll(".column")
      console.info(`%c  .column: ${this.refs.columnsList}  `, "color: #ff9800; font-weight: bold; background-color: black")
      
      this.run()
    } catch (ex) { }
  }

  run = () => {
    this.refs.columnsList.forEach(column => {
      console.info(`%c  COLUMN FOUND  `, "color: #ff9800; font-weight: bold; background-color: black")
      const buttons = column?.querySelectorAll('hui-button-card')
      buttons.forEach(button => {
        console.info(`%c  ${button}  `, "color: #ff9800; font-weight: bold; background-color: black")
      })

      buttons.forEach(button => {
        button.addEventListener('click', () => {
          console.info(`%c  BUTTON AUDIO  `, "color: #ff9800; font-weight: bold; background-color: black")
          // Play the audio file when the button is clicked/tapped
          btnBeep.play();
        });
      });
    })
  }
}

Promise.resolve(customElements.whenDefined('hui-masonry-view')).then(() => {
  console.info(`%c  CALLING Btn CLASS  `, "color: #ff9800; font-weight: bold; background-color: black")
  window.customStyle = new BtnSoundEffects()
})