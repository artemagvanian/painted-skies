<template>
    <div id="app">
        <transition name="fade">
            <router-view></router-view>
        </transition>
    </div>
</template>

<script>
    import Vue from 'vue'
    import BootstrapVue from 'bootstrap-vue'
    import VueRouter from 'vue-router'

    import MindmapViewer from './components/MindmapViewer'
    import PdfUploader from './components/PdfUploader'
    import ImageUploader from './components/ImageUploader'
    import CanvasSelector from './components/CanvasSelector'
    import Menu from './components/Menu'

    Vue.use(BootstrapVue);
    Vue.use(VueRouter);

    const routes = [
        {path: '/mindmap-viewer', component: MindmapViewer, props: true, name: "mindmap"},
        {path: '/canvas-selector', component: CanvasSelector, props: true, name: "canvas"},
        {path: '/', component: Menu},
        {path: '/pdf-uploader', component: PdfUploader, name: "pdf"},
        {path: '/image-uploader', component: ImageUploader, name: 'image'}
    ];

    const router = new VueRouter({
        routes
    });

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
        faArrowRight,
        faFilePdf,
        faFileImage
    } from '@fortawesome/free-solid-svg-icons'
    import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'

    library.add(
        faArrowsAlt,
        faPen,
        faHandPointer,
        faTimes,
        faSearchPlus,
        faSearchMinus,
        faArrowRight,
        faFilePdf,
        faFileImage
    );

    Vue.component('font-awesome-icon', FontAwesomeIcon);

    import Raven from 'raven-js';
    import RavenVue from 'raven-js/plugins/vue';

    Raven
        .config('https://01b7ac134bec4864955f639cfc40bfab@sentry.io/1270071')
        .addPlugin(RavenVue, Vue)
        .install();

    export default {
        router,
        name: 'app',
    }
</script>

<style>
    html, body, #app {
        height: 100%;
    }

    * {
        box-sizing: border-box;
    }

    body {
        margin: 0;
    }

    /*To make canvas margin work*/
    .canvas-container {
        position: fixed !important;
        bottom: 0;
        left: 0;
    }

    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }

    .fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */
    {
        opacity: 0;
    }
</style>
