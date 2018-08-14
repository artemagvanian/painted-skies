<template>
    <div id="canvas-selector">
        <div class="top-menu">
            <nav>
                <b-button-group>
                    <b-button @click="setMode('pan')" :variant="mode === 'pan' ? 'primary' : 'secondary'">
                        <font-awesome-icon icon="arrows-alt"/>
                    </b-button>
                    <b-button @click="setMode('drw')" :variant="mode === 'drw' ? 'primary' : 'secondary'">
                        <font-awesome-icon icon="pen"/>
                    </b-button>
                    <b-button @click="setMode('sel')" :variant="mode === 'sel' ? 'primary' : 'secondary'">
                        <font-awesome-icon icon="hand-pointer"/>
                    </b-button>
                </b-button-group>
                <b-button @click="deleteActive()" :disabled="mode !== 'sel'">
                    <font-awesome-icon icon="times"/>
                </b-button>
                <b-button-group>
                    <b-button :variant="color === 'rgba(255,0,0,.5)' && mode === 'drw' ? 'danger' : 'secondary'"
                              @click="setBrushColor('rgba(255,0,0,.5)')">1
                    </b-button>
                    <b-button :variant="color === 'rgba(0,255,0,.5)' && mode === 'drw' ? 'success' : 'secondary'"
                              @click="setBrushColor('rgba(0,255,0,.5)')">2
                    </b-button>
                    <b-button :variant="color === 'rgba(0,0,255,.5)' && mode === 'drw' ? 'primary' : 'secondary'"
                              @click="setBrushColor('rgba(0,0,255,.5)')">3
                    </b-button>
                </b-button-group>
                <b-button-group>
                    <b-button @click="zoomIn()">
                        <font-awesome-icon icon="search-plus"/>
                    </b-button>
                    <b-button @click="zoomOut()">
                        <font-awesome-icon icon="search-minus"/>
                    </b-button>
                </b-button-group>
                <b-button @click="saveImage()">
                    <font-awesome-icon icon="arrow-right"/>
                </b-button>
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
        data() {
            return {
                canvas: null,
                mode: 'sel', // can be 'sel' = selection, 'pan' = panning, 'drw' = 'drawing'
                color: 'rgba(255,0,0,.5)',
                zoom: 1,
            }
        },
        mounted() {

            //Дабы использовать текущий контекст внутри функции
            let self = this,
                scrollbarWidth = this.getScrollBarWidth(),
                topBarHeight = 50,
                w = $(document).width() - scrollbarWidth,
                h = $(document).height() - topBarHeight;

            //Тестовое изображение. Потом будет загружаться пользователем

            let article = "https://www.latextemplates.com/wp-content/uploads/2012/08/article_1.jpg";

            //Формирование канваса для рисования пользователем по нему
            fabric.Image.fromURL(article, function (img) {
                    // Создание самого канваса
                    self.canvas = new fabric.Canvas('image-selector', {
                        width: w,
                        height: h,
                        backgroundColor: null,
                    });

                    //Установить фон
                    self.canvas.setBackgroundImage(img, self.canvas.renderAll.bind(self.canvas), {
                        scaleX: self.canvas.width / img.width,
                        scaleY: self.canvas.width / img.width,
                    });

                    let canvas = self.canvas, rect, isDown, origX, origY;

                    //Добавить обработчики всяких событий (рисование, перемещение)
                    canvas.on('mouse:down', function (o) {
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

                    canvas.on('mouse:move', function (e) {
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

                    canvas.on('mouse:up', function () {
                        if (self.mode === 'drw') {
                            isDown = false;
                            self.canvas.discardActiveObject().renderAll();
                        }
                    });

                    canvas.on('touch:drag', function (e) {
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
                        }
                    });
                }
            );
        },
        methods: {
            getScrollBarWidth() {
                let inner = document.createElement('p');
                inner.style.width = "100%";
                inner.style.height = "200px";

                let outer = document.createElement('div');
                outer.style.position = "absolute";
                outer.style.top = "0px";
                outer.style.left = "0px";
                outer.style.visibility = "hidden";
                outer.style.width = "200px";
                outer.style.height = "150px";
                outer.style.overflow = "hidden";
                outer.appendChild(inner);

                document.body.appendChild(outer);
                let w1 = inner.offsetWidth;
                outer.style.overflow = 'scroll';
                let w2 = inner.offsetWidth;

                if (w1 === w2) {
                    w2 = outer.clientWidth;
                }

                document.body.removeChild(outer);

                return (w1 - w2);
            }
            ,
            deleteActive() {
                let activeObjects = this.canvas.getActiveObjects();
                this.canvas.discardActiveObject();
                let canvas = this.canvas;
                activeObjects.forEach(function (object) {
                    canvas.remove(object);
                });
            }
            ,
            setMode(mode) {
                this.mode = mode;
                this.canvas.selection = mode !== 'pan';
            }
            ,
            setBrushColor(color) {
                this.color = color;
                this.setMode('drw');
            }
            ,
            zoomIn() {
                this.zoom = this.zoom * 1.5 > 15 ? this.zoom : this.zoom * 1.5;
                this.canvas.setZoom(this.zoom);
            }
            ,
            zoomOut() {
                this.zoom = this.zoom / 1.5 < 1 ? this.zoom : this.zoom / 1.5;
                this.canvas.setZoom(this.zoom);
            }
            ,
            saveImage() {
                console.log(JSON.stringify(this.canvas));
            }
        }
        ,
    }
</script>

<style scoped>
    button {
        padding: 5px 15px;
        margin: 5px 0;
    }

    nav {
        max-width: calc(100vw - 150px);
        display: flex;
        justify-content: space-around;
        margin: 0 auto;
    }

    .top-menu {
        position: fixed;
        z-index: 1000;
        background-color: rgba(195, 225, 244, .5);
        top: 0;
        width: 100vw;
        height: 50px;
    }

</style>