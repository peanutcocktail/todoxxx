module.exports = {
  version: "2.0",
  title: "Todo App",
  description: "Lightweight, local-first todo list powered by FastAPI.",
  icon: "icon.svg",
  menu: async (kernel, info) => {
    const installed = info.exists("app/venv")
    const running = {
      install: info.running("install.js"),
      start: info.running("start.js"),
      update: info.running("update.js"),
      reset: info.running("reset.js")
    }

    if (running.install) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Installing",
        href: "install.js",
      }]
    }

    if (!installed) {
      return [{
        default: true,
        icon: "fa-solid fa-plug",
        text: "Install",
        href: "install.js",
      }]
    }

    if (running.start) {
      const local = info.local("start.js")
      if (local && local.url) {
        return [{
          default: true,
          icon: "fa-solid fa-rocket",
          text: "Open Web UI",
          href: local.url,
        }, {
          icon: "fa-solid fa-terminal",
          text: "Terminal",
          href: "start.js",
        }]
      }
      return [{
        default: true,
        icon: "fa-solid fa-terminal",
        text: "Terminal",
        href: "start.js",
      }]
    }

    if (running.update) {
      return [{
        default: true,
        icon: "fa-solid fa-rotate-right",
        text: "Updating",
        href: "update.js",
      }]
    }

    if (running.reset) {
      return [{
        default: true,
        icon: "fa-regular fa-circle-xmark",
        text: "Resetting",
        href: "reset.js",
      }]
    }

    return [{
      default: true,
      icon: "fa-solid fa-power-off",
      text: "Start",
      href: "start.js",
    }, {
      icon: "fa-solid fa-plug",
      text: "Install",
      href: "install.js",
    }, {
      icon: "fa-solid fa-rotate-right",
      text: "Update",
      href: "update.js",
    }, {
      icon: "fa-regular fa-circle-xmark",
      text: "Reset",
      href: "reset.js",
    }]
  }
}
