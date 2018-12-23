<template>
    <div id="menu">
        <b-container class="d-flex justify-content-center flex-column h-100">
            <h1 class="text-center mb-5">{{ caption }}</h1>
            <b-row class="text-center w-100">
                <router-link :to="{name:'pdf'}" tag="div" class="col btn btn-primary p-5 m-2">
                    <font-awesome-icon icon="file-pdf"/>
                    <p>PDF</p>
                </router-link>
                <router-link :to="{name:'image'}" tag="div" class="col btn btn-primary p-5 m-2">
                    <font-awesome-icon icon="file-image"/>
                    <p>Картинка</p>
                </router-link>
                <router-link :to="{name:'list'}" tag="div" class="col btn btn-primary p-5 m-2">
                    <font-awesome-icon icon="book"/>
                    <p>Бібліотека</p>
                </router-link>
                <router-link :to="{name: loggedIn ? 'logout' : 'login'}" tag="div" class="col btn btn-primary p-5 m-2">
                    <font-awesome-icon icon="book"/>
                    <p>{{ loggedIn ? 'Вийти' : 'Увійти'}}</p>
                </router-link>
            </b-row>
        </b-container>
    </div>
</template>

<script>
    import Auth from '../utils/auth'

    export default {
        data() {
            return {
                caption: "",
                loggedIn: false,
            }
        },
        mounted() {
            Auth.verify(this.$session).then((response) => {
                if (response) {
                    this.caption = 'Привіт, ' + Auth.getUserInfo(this.$session).username;
                    this.loggedIn = true;
                } else {
                    this.caption = 'Привіт, незнайомцю!';
                }
            })
        },
        name: "Menu"
    }
</script>

<style scoped>
    #menu {
        height: 100%;
    }

    .btn {
        font-size: 30px;
        display: block;
    }
</style>