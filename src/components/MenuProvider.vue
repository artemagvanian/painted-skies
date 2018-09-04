<template>
    <div id="menu-provider">
        <component :is="currentTabComponent"></component>
        <div class="spin" v-if="loading">
            <div class="cp-spinner cp-heart"></div>
        </div>
        <b-modal id="modal" v-model="modalShow" title="Сталася помилка!" ok-only="true">
            Вся команда розробників вже знає про це та намагається все виправити. Зверніть увагу, що наш сервер не
            оброблює зображення, більші за 10 МБ. Якщо виділень на конспекті дуже багато та сервер завантажений, можуть
            статися помилки. Спробуйте оновити сторінку!
        </b-modal>
    </div>
</template>

<script>
    import CanvasSelector from './CanvasSelector.vue'
    import MindmapViewer from './MindmapViewer.vue'
    import ImageUploader from './ImageUploader.vue'
    import Raven from 'raven-js';
    import $ from 'jquery';
    import 'csspin/css/csspin-heart.css'


    export default {
        name: "MenuProvider",
        components: {
            CanvasSelector,
            MindmapViewer,
            ImageUploader
        },
        data() {
            return {
                tabs: ['ImageUploader', 'CanvasSelector', 'MindmapViewer'],
                currentTabNumber: 0,
                image: null,
                mindmap: null,
                lang: null,
                loading: false,
                modalShow: false,
            }
        },
        methods: {
            switchCurrentTab(tabNumber) {
                this.currentTabNumber = tabNumber;
            },
            getMindmap(canvas, lang) {
                // let data = JSON.stringify({
                //     'canvas': canvas
                // });
                return $.post(
                    '/api/note',
                    {'canvas': canvas, 'lang': lang}
                )
            }
        },
        computed: {
            currentTabComponent() {
                return this.tabs[this.currentTabNumber];
            }
        },
        mounted() {
            let vm = this;
            this.$root.$on('imageUploaded', function (obj) {
                vm.image = obj.image;
                vm.lang = obj.lang;
                vm.switchCurrentTab(1);
            });
            this.$root.$on('imageColored', function (canvas) {
                vm.loading = true;
                vm.getMindmap(canvas, vm.lang).then((response) => {
                    vm.mindmap = response;
                    vm.switchCurrentTab(2);
                    vm.loading = false;
                }).catch((e) => {
                    vm.loading = false;
                    Raven.captureException(e);
                    vm.modalShow = true;
                });
            });
        }
    }
</script>

<style scoped>
    .spin {
        position: fixed;
        display: flex;
        width: 100vw;
        height: 100vh;
        top: 0;
        left: 0;
        z-index: 1000;
        justify-content: center;
        align-items: center;
        background-color: rgba(128, 128, 128, .5);
    }
</style>