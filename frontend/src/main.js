import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false;

import VueSession from 'vue-session'

Vue.use(VueSession);

import Vuetify from 'vuetify'
import 'vuetify/dist/vuetify.min.css'
import 'material-design-icons-iconfont/dist/material-design-icons.css'

Vue.use(Vuetify, {
    iconfont: 'md'
});


import * as Sentry from '@sentry/browser'
import VueAnalytics from 'vue-analytics'

if (process.env.NODE_ENV === 'production') {
    Sentry.init({
        dsn: process.env.VUE_APP_SENTRY_PUBLIC_DSN,
        integrations: [new Sentry.Integrations.Vue({Vue})]
    });

    Vue.use(VueAnalytics, {
        id: process.env.VUE_APP_GOOGLE_ANALYTICS,
        router
    });
}

new Vue({
    router,
    render: h => h(App)
}).$mount('#app');
