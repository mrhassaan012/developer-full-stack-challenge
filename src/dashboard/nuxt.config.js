export default {
    // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
    ssr: false,
    middleware: ['auth-login-redirect'],


    // Target: https://go.nuxtjs.dev/config-target
    target: 'static',

    // Global page headers: https://go.nuxtjs.dev/config-head
    head: {
        title: 'DC Full Stack Code Challenge',
        htmlAttrs: {
            lang: 'en',
        },
        meta: [
            { charset: 'utf-8' },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1',
            },
            { hid: 'description', name: 'description', content: '' },
            { name: 'format-detection', content: 'telephone=no' },
        ],
        link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
    },

    // Global CSS: https://go.nuxtjs.dev/config-css
    css: [],

    // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
    plugins: [],

    // Auto import components: https://go.nuxtjs.dev/config-components
    components: true,

    pages: true,

    // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
    buildModules: [
        // https://go.nuxtjs.dev/typescript
        '@nuxt/typescript-build',
    ],

    // Modules: https://go.nuxtjs.dev/config-modules
    modules: [
        // https://go.nuxtjs.dev/bootstrap
        ['bootstrap-vue/nuxt', { icons: true, css: true }],
        // https://go.nuxtjs.dev/axios
        '@nuxtjs/axios',
        '@nuxtjs/auth-next',
        '@nuxtjs/toast',
    ],
    toast: {
        position: 'bottom-center',
        duration: 3000,
        theme: "bubble",
    },

    publicRuntimeConfig: {
        axios: {
            baseURL: process.env.BASEURL || 'http://localhost:8000',
        },
    },

    // Axios module configuration: https://go.nuxtjs.dev/config-axios
    axios: {
        // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
        credentials: true,
        baseURL: process.env.NODE_ENV == 'development' ? 'http://localhost:8000' : process.env.BASEURL,
    },
    router: {
        middleware: ['auth'],
    },

    cookie: {
        options: {
            maxAge: 12 * 24 * 60 * 60
        }
    },
    auth: {
        strategies: {
          local: {
            token: {
              property: 'access_token',
              required: true,
              type: 'Bearer',
            },
            endpoints: {
              login: { url: '/auth/token', method: 'post', propertyName: 'access_token' },
              logout: { url: '/auth/logout', method: 'post'},
              user: { url: '/auth/me', method: 'get' },
            },
          },
        },
        redirect: {
          login: '/login',
          logout: '/login', // Redirect to the login page after logout
          home: '/authors',
        }
      },

    // Build Configuration: https://go.nuxtjs.dev/config-build
    build: {},
};
