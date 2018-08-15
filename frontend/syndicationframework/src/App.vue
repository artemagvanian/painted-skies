<template>
    <div id="app">
        <MenuProvider/>
    </div>
</template>

<script>
    import Vue from 'vue'
    import BootstrapVue from 'bootstrap-vue'

    Vue.use(BootstrapVue);

    import 'bootstrap/dist/css/bootstrap.css'
    import 'bootstrap-vue/dist/bootstrap-vue.css'

    import {library} from '@fortawesome/fontawesome-svg-core'
    import {
        faArrowsAlt,
        faPen,
        faHandPointer,
        faTimes,
        faSearchPlus,
        faSearchMinus,
        faArrowRight
    } from '@fortawesome/free-solid-svg-icons'
    import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

    library.add(
        faArrowsAlt,
        faPen,
        faHandPointer,
        faTimes,
        faSearchPlus,
        faSearchMinus,
        faArrowRight
    );

    Vue.component('font-awesome-icon', FontAwesomeIcon);

    import MenuProvider from './components/MenuProvider.vue'

    export default {
        name: 'app',
        components: {
            MenuProvider
        }
    }
</script>

<style>
    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
    }

    /*To make canvas margin work*/
    .canvas-container {
        margin-top: 50px !important;
    }
</style>
