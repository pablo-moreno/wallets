import theme from "@nuxt/content-theme-docs"

export default theme({
  /*
   ** You can extend the nuxt configuration
   ** Doc: https://content.nuxtjs.org/themes-docs#nuxtconfigjs
   */
  i18n: {
    locales: () => [{
      code: 'es',
      iso: 'es-ES',
      file: 'es-ES.js',
      name: 'Castellano'
    }],
    defaultLocale: 'es'
  }
})