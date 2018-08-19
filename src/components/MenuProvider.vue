<template>
    <div id="menu-provider">
        <keep-alive>
            <component :is="currentTabComponent"></component>
        </keep-alive>
        <div class="spin" v-if="loading">
            <div class="cp-spinner cp-heart"></div>
        </div>
    </div>
</template>

<script>
    import CanvasSelector from './CanvasSelector.vue'
    import MindmapViewer from './MindmapViewer.vue'
    import ImageUploader from './ImageUploader.vue'
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
                loading: false
            }
        },
        methods: {
            switchCurrentTab(tabNumber) {
                this.currentTabNumber = tabNumber;
            },
            getMindmap(canvas) {
                // let data = JSON.stringify({
                //     'canvas': canvas
                // });
                return $.post(
                    'https://syndication-framework.herokuapp.com/api/note',
                    {'canvas': canvas}
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
            this.$root.$on('imageUploaded', function (image) {
                vm.image = image;
                vm.switchCurrentTab(1);
            });
            this.$root.$on('imageColored', function (canvas) {
                vm.loading = true;
                vm.getMindmap(canvas).then((response) => {
                    vm.mindmap = response;
                    vm.switchCurrentTab(2);
                    vm.loading = false;
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