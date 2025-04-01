async function load_event_language_switcher() {
  function getQueryParam(param) {
    let urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
  }

  function redirectUrlLang(lang) {
    let newUrl = new URL(window.location);
    newUrl.searchParams.set("lang", lang);
    window.location.href = newUrl;
  }

  function getCookie(name) {
    let matches = document.cookie.match(
      new RegExp("(^| )" + name + "=([^;]+)")
    );
    return matches ? decodeURIComponent(matches[2]) : null;
  }

  async function getLanguageUser() {
    if (getCookie("user_id") && getCookie("user_id") != "Guest") {
      await frappe.call({
        method: "wiki.api.get_language",
        callback: function (r) {
          if (r.message) {
            if (!lang) lang = r.message;
          }
        },
      });
    }
  }

  async function setLanguageUser(lang, reload = true) {
    if (getCookie("user_id") && getCookie("user_id") != "Guest") {
      await frappe.call({
        method: "wiki.api.change_language",
        args: {
          lang: lang,
        },
        callback: function (r) {
          if (reload) redirectUrlLang(lang);
        },
      });
    } else {
      redirectUrlLang(lang);
    }
  }

  let lang = getQueryParam("lang");
  if (!lang) {
    await getLanguageUser();
  } else {
    setLanguageUser(lang, false);
  }

  // web
  document.getElementById("language-switcher-web").value = lang;
  document
    .getElementById("language-switcher-web")
    .addEventListener("change", function () {
      setLanguageUser(this.value);
    });

  // mobile
  document.getElementById("language-switcher-mobi").value = lang;
  document
    .getElementById("language-switcher-mobi")
    .addEventListener("change", function () {
      setLanguageUser(this.value);
    });
}

load_event_language_switcher();
