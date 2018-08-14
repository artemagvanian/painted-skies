<template>
    <div id="app">
        <CanvasSelector/>
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

    library.add(faArrowsAlt, faPen, faHandPointer, faTimes, faSearchPlus, faSearchMinus, faArrowRight);

    Vue.component('font-awesome-icon', FontAwesomeIcon);

    import CanvasSelector from './components/CanvasSelector.vue'

    export default {
        name: 'app',
        components: {
            CanvasSelector
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
