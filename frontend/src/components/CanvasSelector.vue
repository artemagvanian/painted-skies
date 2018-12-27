<template>
    <div id="canvas-selector">
        <div class="top-menu">
            <nav>
                <b-button-group data-hint='Use these buttons to change mode. There are pan, draw and select options'
                                data-hintPosition="bottom-right">
                    <b-button v-for="button in modeButtons" @click="setMode(button.mode)"
                              :variant="mode === button.mode ? 'primary' : 'secondary'">
                        <font-awesome-icon :icon="button.icon"/>
                    </b-button>
                </b-button-group>
                <b-button @click="deleteActive()" :disabled="mode !== 'sel'"
                          data-hint='Remove bad selections using this button. Only available in select mode'
                          data-hintPosition="bottom-right">
                    <font-awesome-icon icon="times"/>
                </b-button>
                <b-button-group data-hint='Change levels of mindmap using these buttons'
                                data-hintPosition="bottom-right">
                    <b-button :variant="color === 'rgba(255,0,0,.5)' && mode === 'drw' ? 'danger' : 'secondary'"
                              @click="setBrushColor('rgba(255,0,0,.5)')"
                              :disabled="!redCanBeActive">
                        1
                    </b-button>
                    <b-button :variant="color === 'rgba(0,255,0,.5)' && mode === 'drw' ? 'success' : 'secondary'"
                              @click="setBrushColor('rgba(0,255,0,.5)')"
                              :disabled="!greenCanBeActive">
                        2
                    </b-button>
                    <b-button :variant="color === 'rgba(0,0,255,.5)' && mode === 'drw' ? 'primary' : 'secondary'"
                              @click="setBrushColor('rgba(0,0,255,.5)')"
                              :disabled="!blueCanBeActive">
                        3
                    </b-button>
                </b-button-group>
                <b-button-group data-hint='Use these buttons to zoom'
                                data-hintPosition="bottom-right">
                    <b-button @click="zoomIn()">
                        <font-awesome-icon icon="search-plus"/>
                    </b-button>
                    <b-button @click="zoomOut()">
                        <font-awesome-icon icon="search-minus"/>
                    </b-button>
                </b-button-group>
                <router-link :to="{
                    name: 'mindmap',
                    params: { canvas: JSON.stringify(this.canvas), lang: this.lang }
                }" tag="div">
                    <b-button data-hint='When you are ready, press this button to get mindmap'
                              data-hintPosition="bottom-right">
                        <font-awesome-icon icon="arrow-right"/>
                    </b-button>
                </router-link>
            </nav>
        </div>
        <canvas id="image-selector"></canvas>
    </div>
</template>

<script>
    import {fabric} from 'fabric-with-gestures';
    import $ from 'jquery';


    export default {
        name: "CanvasSelector",
        props: ['image', 'lang'],
        data() {
            return {
                canvas: null,
                mode: 'sel', // can be 'sel' = selection, 'pan' = panning, 'drw' = 'drawing'
                color: 'rgba(255,0,0,.5)',
                zoom: 1,
                modeButtons: [
                    {mode: "pan", icon: "arrows-alt"},
                    {mode: "drw", icon: "pen"},
                    {mode: "sel", icon: "hand-pointer"}
                ]
            }
        },
        mounted() {
            let topBarHeight = 100,
                w = window.innerWidth
                    || document.documentElement.clientWidth
                    || document.body.clientWidth,

                h = window.innerHeight
                    || document.documentElement.clientHeight
                    || document.body.clientHeight;

            console.log(w, h);

            this.canvas = new fabric.Canvas('image-selector', {
                width: w,
                height: h - topBarHeight,
                backgroundColor: null,
            });

            let canvas = this.canvas,
                self = this,
                rect,
                isDown,
                origX,
                origY;

            //Добавить обработчики всяких событий (рисование, перемещение)
            this.canvas.on('mouse:down', function (o) {
                if (self.mode === 'drw') {
                    isDown = true;
                    var pointer = canvas.getPointer(o.e);
                    origX = pointer.x;
                    origY = pointer.y;
                    pointer = canvas.getPointer(o.e);
                    rect = new fabric.Rect({
                        left: origX,
                        top: origY,
                        originX: 'left',
                        originY: 'top',
                        width: pointer.x - origX,
                        height: pointer.y - origY,
                        angle: 0,
                        fill: self.color,
                        transparentCorners: false
                    });
                    canvas.add(rect);
                }
            });

            this.canvas.on('mouse:move', function (e) {
                if (self.mode === 'drw') {
                    if (!isDown) return;
                    var pointer = canvas.getPointer(e.e);

                    if (origX > pointer.x) {
                        rect.set({left: Math.abs(pointer.x)});
                    }
                    if (origY > pointer.y) {
                        // noinspection JSSuspiciousNameCombination
                        rect.set({top: Math.abs(pointer.y)});
                    }

                    rect.set({width: Math.abs(origX - pointer.x)});
                    rect.set({height: Math.abs(origY - pointer.y)});

                    canvas.renderAll();
                }
            });

            this.canvas.on('mouse:up', function () {
                if (self.mode === 'drw') {
                    isDown = false;
                    self.canvas.discardActiveObject().renderAll();
                }
            });

            let article = this.image;

            this.canvas.on('touch:drag', function (e) {
                if (self.mode === 'pan') {
                    this.currentX = e.self.x;
                    this.currentY = e.self.y;
                    let xChange = this.currentX - this.lastX;
                    let yChange = this.currentY - this.lastY;

                    // noinspection JSSuspiciousNameCombination
                    if ((Math.abs(xChange) <= 50) && (Math.abs(yChange) <= 50)) {
                        var delta = new fabric.Point(xChange, yChange);
                        canvas.relativePan(delta);
                    }

                    this.lastX = e.self.x;
                    this.lastY = e.self.y;

                    if (this.viewportTransform[4] >= 0) {
                        this.viewportTransform[4] = 0;
                    }

                    if (this.viewportTransform[5] >= 0) {
                        this.viewportTransform[5] = 0;
                    }

                    if (this.viewportTransform[4] <= -canvas.backgroundImage.getScaledWidth() * canvas.getZoom() + canvas.getWidth()) {
                        this.viewportTransform[4] = -canvas.backgroundImage.getScaledWidth() * canvas.getZoom() + canvas.getWidth();
                    }

                    if (this.viewportTransform[5] <= -canvas.backgroundImage.getScaledHeight() * canvas.getZoom() + canvas.getHeight()) {
                        this.viewportTransform[5] = -canvas.backgroundImage.getScaledHeight() * canvas.getZoom() + canvas.getHeight();
                    }
                }
            });

            fabric.Image.fromURL(article,
                function (img) {
                    let scale = Math.max(self.canvas.width / img.width, self.canvas.height / img.height);

                    self.canvas.setBackgroundImage(img, self.canvas.renderAll.bind(self.canvas), {
                        scaleX: scale,
                        scaleY: scale,
                    });
                }
            );
            //introJs().addHints();
        },
        methods: {
            deleteActive() {
                let activeObjects = this.canvas.getActiveObjects();
                this.canvas.discardActiveObject();
                let canvas = this.canvas;
                activeObjects.forEach(function (object) {
                    if (object.fill === 'rgba(255,0,0,.5)') {
                        canvas.remove(...canvas.getObjects());
                    }
                    canvas.remove(object);
                });
            },
            setMode(mode) {
                this.mode = mode;
                this.canvas.selection = mode !== 'pan';
            },
            setBrushColor(color) {
                this.color = color;
                this.setMode('drw');
            },
            zoomIn() {
                this.zoom = this.zoom * 1.5 > 15 ? this.zoom : this.zoom * 1.5;
                this.canvas.setZoom(this.zoom);
            },
            zoomOut() {
                this.zoom = this.zoom / 1.5 < 1 ? this.zoom : this.zoom / 1.5;
                this.canvas.setZoom(this.zoom);
            },
            // saveImage() {
            //     this.$root.$emit('imageColored', JSON.stringify(this.canvas));
            // }
        },
        computed: {
            lastRectangleColor() {
                try {
                    let objects = this.canvas.getObjects();
                    if (objects.length === 0) {
                        this.setBrushColor('rgba(255,0,0,.5)');
                    } else if (objects[objects.length - 1].fill === 'rgba(255,0,0,.5)') {
                        this.setBrushColor('rgba(0,255,0,.5)');
                    }
                    return objects[objects.length - 1].fill;
                } catch (e) {
                    return null;
                }
            },
            redCanBeActive() {
                return this.lastRectangleColor == null;
            },
            greenCanBeActive() {
                return this.lastRectangleColor != null;
            },
            blueCanBeActive() {
                return this.lastRectangleColor === 'rgba(0,255,0,.5)' || this.lastRectangleColor === 'rgba(0,0,255,.5)';
            }
        }
    }
</script>

<style scoped>
    button {
        padding: 5px 15px;
        margin: 5px 0;
    }

    nav {
        max-width: 100vw;
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
        margin: 0 auto;
        height: 100px;
        align-items: center;
    }

    .top-menu {
        position: fixed;
        /*z-index: 100;*/
        background-color: rgba(195, 225, 244, .5);
        top: 0;
        width: 100vw;
        height: 100px;
    }

</style>