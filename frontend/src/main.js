import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false;

import BootstrapVue from 'bootstrap-vue'
import VueSession from 'vue-session'

Vue.use(VueSession);
Vue.use(BootstrapVue);

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import {library} from '@fortawesome/fontawesome-svg-core'
import {
    faArrowsAlt,
    faPen,
    faHandPointer,
    faSearchPlus,
    faSearchMinus,
    faArrowRight,
    faFilePdf,
    faFileImage,
    faBook,
    faBackspace,
    faPlus,
} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

library.add(
    faArrowsAlt,
    faPen,
    faHandPointer,
    faSearchPlus,
    faSearchMinus,
    faArrowRight,
    faFilePdf,
    faFileImage,
    faBook,
    faBackspace,
    faPlus,
);

Vue.component('font-awesome-icon', FontAwesomeIcon);

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
