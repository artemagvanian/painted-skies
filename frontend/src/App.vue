<template>
    <div id="app">
        <transition name="fade">
            <router-view></router-view>
        </transition>
    </div>
</template>

<script>
    import $ from 'jquery'
    import 'jquery.cookie/jquery.cookie'

    export default {
        name: 'app',
        mounted() {
            $.ajax({
                url: '/api/csrf',
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    $.cookie('csrftoken', data.token);
                }
            });
        }
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
