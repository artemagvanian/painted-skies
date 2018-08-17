<template>
    <div id="menu-provider">
        <keep-alive>
            <component :is="currentTabComponent"></component>
        </keep-alive>
    </div>
</template>

<script>
    import CanvasSelector from './CanvasSelector.vue'
    import MindmapViewer from './MindmapViewer.vue'
    import ImageUploader from './ImageUploader.vue'
    import $ from 'jquery';

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
                mindmap: null
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
                    'http://localhost:8000/api/note',
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
                vm.getMindmap(canvas).then((response) => {
                    vm.mindmap = response;
                    vm.switchCurrentTab(2);
                });
            });
        }
    }
</script>

<style scoped>

</style>