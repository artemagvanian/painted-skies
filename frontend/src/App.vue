<template>
    <v-app>
        <v-navigation-drawer right app v-model="drawer" temporary>
            <v-list>
                <v-list-tile :to="{name:'pdf'}">
                    <v-list-tile-action>
                        <v-icon>picture_as_pdf</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Конспектувати з PDF</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <v-divider></v-divider>
                <v-list-tile :to="{name:'image'}">
                    <v-list-tile-action>
                        <v-icon>image</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Конспектувати з картинки</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <v-divider></v-divider>
                <v-list-tile :to="{name:'mindmap'}">
                    <v-list-tile-action>
                        <v-icon>brush</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>Створити конспект з нуля</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
                <template v-if="Auth.loggedIn">
                    <v-divider></v-divider>
                    <v-list-tile :to="{name:'list'}">
                        <v-list-tile-action>
                            <v-icon>book</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Бібліотека</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </template>
                <template v-else>
                    <v-divider></v-divider>
                    <v-list-tile :to="{name:'signup'}">
                        <v-list-tile-action>
                            <v-icon>arrow_upward</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Зареєструватися</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </template>
                <v-divider></v-divider>
                <v-list-tile :to="{name: Auth.loggedIn ? 'logout' : 'login'}">
                    <v-list-tile-action>
                        <v-icon>arrow_forward</v-icon>
                    </v-list-tile-action>
                    <v-list-tile-content>
                        <v-list-tile-title>{{ Auth.loggedIn ? 'Вийти' : 'Увійти'}}</v-list-tile-title>
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
        </v-navigation-drawer>
        <v-toolbar app prominent flat>
            <v-toolbar-title>Painted Skies</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon>
                <v-icon>info</v-icon>
            </v-btn>
            <v-btn icon @click="drawer = !drawer">
                <v-icon>menu</v-icon>
            </v-btn>
        </v-toolbar>
        <v-content>
            <router-view></router-view>
        </v-content>
    </v-app>
</template>

<script>
    import $ from 'jquery'
    import 'jquery.cookie/jquery.cookie'
    import Auth from './utils/auth'

    export default {
        name: 'app',
        data() {
            return {
                drawer: false,
                Auth,
            }
        },
        mounted() {
            $.ajax({
                url: '/api/csrf',
                type: 'GET',
                dataType: 'json',
                success: function (data) {
                    $.cookie('csrftoken', data.token);
                }
            });
            Auth.verify(this.$session)
        }
    }
</script>